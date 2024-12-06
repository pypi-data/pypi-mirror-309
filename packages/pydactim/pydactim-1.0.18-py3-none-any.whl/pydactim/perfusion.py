import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from tqdm.contrib import tzip
from scipy.optimize import minimize
from scipy.linalg import block_diag
import warnings
from tqdm import tqdm

class SignalDSC():
    def __init__(self, dsc_path, brain_mask_path, aif_mask_path=None, baseline=8, offset=0, r2=1, TE=0.03, nobar=True, plot=False):
        self.baseline = baseline
        self.r2 = r2
        self.TE = TE
        self.kH = 0.1369 * (0.55 / 0.75) # Constant grouping tissular parameters for absolute quantification
        self.rho_Voi = 0.0104  # Apparent brain density [100g/ml]
        self.hematocrit = self.kH / self.rho_Voi
        self.offset = offset
        self.plot = plot

        functions = [
            (self.load_dsc, dsc_path, "Loading DSC data"),
            (self.load_brain_mask, brain_mask_path, "Loading brain mask"),
            (self.load_aif_mask, aif_mask_path, "Loading AIF mask"),
            (self.load_signal_in_brain_mask, None, "Extracting DSC signals among the brain mask")
        ]

        if nobar:
            self.load_dsc(dsc_path)
            self.load_brain_mask(brain_mask_path)
            self.load_aif_mask(aif_mask_path)
            self.load_signal_in_brain_mask()
        else:
            # Create a tqdm progress bar
            with tqdm(total=len(functions), desc="Processing DSC-MRI Perfusion data") as pbar:
                for func, arg, desc in functions:
                    pbar.set_description(f"Processing DSC-MRI Perfusion data - {desc}")
                    if arg is not None:
                        func(arg) 
                    else:
                        func()
                    pbar.update(1) 
 
    def load_dsc(self, dsc_path):
        self.dsc_path = dsc_path
        self.dsc = nib.load(dsc_path)
        self.dsc_data = self.dsc.get_fdata()
        self.size = self.dsc_data.shape[-1]

    def load_brain_mask(self, brain_mask_path):
        self.brain_mask_path = brain_mask_path
        self.brain_mask = nib.load(brain_mask_path)
        self.brain_mask_data = self.brain_mask.get_fdata().astype(bool)
        self.affine = self.brain_mask.affine

    def load_aif_mask(self, aif_mask_path):
        self.aif_mask_path = aif_mask_path
        self.aif_mask = nib.load(aif_mask_path)
        self.aif_mask_data = self.aif_mask.get_fdata().astype(bool)

        self.aif_coord = np.argwhere(self.aif_mask_data > 0)
        self.AIF = np.mean([self.dsc_data[aif[0], aif[1], aif[2], :] for aif in self.aif_coord], axis=0)[self.offset:]
        self.AIF_0 = np.mean(self.AIF[:self.baseline])
        self.Ca = - np.log(self.AIF / self.AIF_0 + 1e-9) / (self.r2 * self.TE)
        self.Ca = np.where(self.Ca < 0., 0, self.Ca)
        self.Ca_0 = np.mean(self.Ca[:self.baseline])

        self.Ca_gamma = self.gamma_variate_fitting(plot=self.plot)

    def load_signal_in_brain_mask(self):
        self.S = self.dsc_data[:,:,:,self.offset:]
        self.S_0 = np.mean(self.dsc_data[:, :, :, self.offset:self.baseline], axis=-1)

        self.S = self.S[self.brain_mask_data]
        self.S_0 = self.S_0[self.brain_mask_data]

    def signal_to_concentration(self, clip=True):
        self.C = - np.log(self.S / np.broadcast_to(self.S_0[:,np.newaxis], self.S.shape) + 1e-9) / (self.r2 * self.TE)
        self.C = np.nan_to_num(self.C, nan=0.)
        if clip: self.C = np.where(self.C < 0, 0., self.C)
    
    def concentration_to_signal(self, aif=False):
        if aif: self.S_revert = self.Ca_0 * np.exp(-self.TE * self.C)
        else: self.S_revert = self.S_0[:, np.newaxis] * np.exp(-self.TE * self.C)
        return self.S_revert

    def gamma_variate_fitting(self, plot=True):

        def gamma_variate(t, t0, r, b, C0):
                tr = t - t0
                y = C0 * (np.sign(tr) * (np.abs(tr)) ** r) * np.exp((-tr) / b)
                return np.where(t > t0, y, 0)

        def gamma_variate_loss(Parameters, Inputs):
            t0 = Parameters[0]
            r = Parameters[1]
            b = Parameters[2]
            C0 = Parameters[3]
            Time = Inputs[0]
            Intensity = Inputs[1]
            Predictions = gamma_variate(Time, t0, r, b, C0)
            return ((Predictions - Intensity) ** 2).mean()

        size = self.Ca.shape[0]
        time_var = np.array([i for i in range(size)])

        dt = 1
        first_derivative = np.diff(self.Ca) / dt

        # Define a threshold
        threshold = np.mean(first_derivative) + 3 * np.std(first_derivative)  # 3-sigma rule

        # Detect the bolus arrival time (BAT)
        try:
            bat_index = np.where(first_derivative > threshold)[0][0]
        except: 
            bat_index = self.baseline
            
        bat_time = time_var[bat_index]

        print(f"BAT: {bat_time}")

        time_var = time_var[:size]
        aif4fitt = self.Ca[:size]

        InputList = [time_var, aif4fitt]

        Optmizer = minimize(
            gamma_variate_loss, [bat_index,1,1,1], InputList,
            # method='nelder-mead',
            # method='SLSQP',
            method='L-BFGS-B',
            options={'xtol': 1e-9, 'disp': False, 'maxiter': 100000}
            )
        t0 = Optmizer.x[0]
        r = Optmizer.x[1]
        b = Optmizer.x[2]
        C0 = Optmizer.x[3]

        fitted_aif = gamma_variate(time_var, bat_index, r, b, C0)

        if plot:
            plt.figure()
            plt.plot(time_var, aif4fitt, 'o')
            plt.plot(time_var, fitted_aif, '-')
            plt.legend(['AIF', 'GammaVariateAIF'])
            plt.xlabel("Time")
            plt.ylabel(r"C$_a$ (t)")
            plt.title("Gamma Variate function fitting output in the time interval [0, {}]".format(size))
            plt.show()
        
        time_var = np.array([i for i in range(size)])
        fitted_aif = gamma_variate(time_var, t0, r, b, C0)

        if plot:
            plt.figure()
            plt.plot(time_var, fitted_aif, '-')
            plt.plot(time_var, self.Ca, 'o', markersize=2)
            plt.legend(['AIF', 'GammaVariateAIF'])
            plt.xlabel("Time")
            plt.ylabel(r"C$_a$ (t)")
            plt.title("Gamma Variate function fitting output in the entire curve")
            plt.show()

        # Once again, but for the AIF fitted
        dt = time_var[1] - time_var[0]
        first_derivative = np.diff(fitted_aif) / dt

        # Define a threshold
        threshold = np.mean(first_derivative) + 3 * np.std(first_derivative)  # 3-sigma rule

        # Detect the bolus arrival time (BAT)
        try:
            bat_index = np.where(first_derivative > threshold)[0][0]
        except: 
            bat_index = self.baseline
        bat_time = time_var[bat_index]

        # Find the peak time (t_peak)
        peak_index = np.argmax(fitted_aif[bat_index:]) + bat_index
        peak_time = time_var[peak_index]

        # Calculate TTP
        ttp = peak_time - bat_time
        cbf = (fitted_aif[peak_index] - fitted_aif[bat_index]) / (peak_time - bat_time)

        # Calculate CBV
        cbv = np.trapz(fitted_aif[bat_index:size], time_var[bat_index:size])

        # Plotting the signal and the detected BAT
        if plot:
            plt.figure(figsize=(10, 5))
            plt.plot(time_var, fitted_aif, label='Signal')
            plt.axvline(bat_time, color='r', linestyle='--', label=f'BAT: {bat_time:.2f} s')
            plt.axvline(peak_time, color='g', linestyle='--', label=f'Peak Time: {peak_time:.2f} s, TTP: {ttp:.2f} s')
            plt.fill_between(time_var[bat_index:], fitted_aif[bat_index:], alpha=0.5, color='orange', label=f'CBV: {cbv:.2f} ua')
            plt.plot([], [], alpha=0, label=f'CBF: {cbf:.2f}')
            plt.plot([], [], alpha=0, label=f'MTT: {(cbv/cbf):.2f}')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Signal Intensity')
            plt.title(f'Bolus Arrival Time Detection in DSC Perfusion MRI')
            plt.legend()
            plt.show()

        return fitted_aif
    
    def solve_CBV(self, clip=True):
        CBV_ = np.trapz(self.C, dx=1, axis=-1) / np.trapz(self.Ca)
        CBV_ = self.hematocrit * CBV_
        self.CBV = np.zeros_like(self.brain_mask_data).astype(np.float32)
        self.CBV[self.brain_mask_data] = CBV_
        if clip: self.CBV = np.where(self.CBV < 0, 0, self.CBV)
        return self.save_image(self.CBV, "pf_CBV")

    def solve_CBF(self):
        self.CBF = np.max(self.TRF, axis=-1)
        self.CBF = self.hematocrit * self.CBF
        return self.save_image(self.CBF * 60, "pf_CBF")

    def solve_MTT(self):
        self.MTT = self.CBV / (self.CBF + 1e-9)
        return self.save_image(self.MTT, "pf_MTT")

    def solve_TTP(self):
        TTP_ = np.array([np.argmax(signal) for signal in self.C]).astype(np.float32)
        self.TTP = np.zeros_like(self.brain_mask_data).astype(np.float32)
        self.TTP[self.brain_mask_data] = TTP_
        return self.save_image(self.TTP, "pf_TTP")

    def solve_Tmax(self, threshold=6.):
        Tmax_ = np.array([np.argmax(signal) for signal in self.TRF_]).astype(np.float32)
        self.Tmax = np.zeros_like(self.brain_mask_data).astype(np.float32)
        self.Tmax[self.brain_mask_data] = Tmax_
        Tmax_ = np.where(self.Tmax < threshold, 0, 1)
        self.save_image(Tmax_, f"pf_Tmax_{str(threshold)}")
        return self.save_image(self.Tmax, "pf_Tmax")
        
    def solve_signal_recovery(self, S_pre, S_post, initial_frame=0):
        self.S_min = np.argmin(np.mean(self.dsc_data, axis=(0,1,2)))
        self.S_pre = [i - initial_frame for i in [initial_frame, S_pre]]
        self.S_post = [i - initial_frame for i in [S_post, self.S.shape[-1]]]

        shifted_S_pre = [i - initial_frame for i in self.S_pre]
        shifted_S_post = [i - initial_frame for i in self.S_post]
        shifted_S_min = self.S_min - initial_frame

        SR_num = np.mean(self.dsc_data[:,:,:,shifted_S_post[0]:shifted_S_post[1]], axis=-1) - np.mean(self.dsc_data[:,:,:,shifted_S_pre[0]:shifted_S_pre[1]], axis=-1)
        SR_denom = np.mean(self.dsc_data[:,:,:,shifted_S_pre[0]:shifted_S_pre[1]], axis=-1)
        self.SR = 100 * SR_num / (SR_denom + 1e-9)

        PSR_num = np.mean(self.dsc_data[:,:,:,shifted_S_post[0]:shifted_S_post[1]], axis=-1) - self.dsc_data[:,:,:,shifted_S_min]
        PSR_denom = np.mean(self.dsc_data[:,:,:,shifted_S_pre[0]:shifted_S_pre[1]], axis=-1) - self.dsc_data[:,:,:,shifted_S_min]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self.PSR = 100 * PSR_num / (PSR_denom + 1e-9)

        self.SR *= self.brain_mask_data
        self.PSR *= self.brain_mask_data
        self.save_image(self.SR, "pf_SR")
        self.save_image(self.PSR, "pf_PSR")

    def solve_deconvolution(self, mode="svd"):
        def _svd(aif):
            temp = np.array([np.roll(aif, i) for i in range(aif.shape[0])]).T
            Lambda = np.tril(temp)
            u, s, vh = np.linalg.svd(Lambda)
            return u, s, vh
        
        def _osvd(aif, oi_threshold=0.1):
            # Create the block-circulant matrix
            n = len(aif)
            aif_padded = np.concatenate([aif, np.zeros(n - 1)])
            Lambda = block_diag(*[np.roll(aif_padded, i)[:n] for i in range(n)])
            
            # Perform SVD
            u, s, vh = np.linalg.svd(Lambda)
            
            # Calculate the oscillation index (OI)
            diags = np.array([np.diag(vh, k) for k in range(-n + 1, n)])
            oscillations = np.sum(np.abs(np.diff(diags, axis=1)), axis=1)
            total_variation = np.sum(np.abs(diags), axis=1)
            oi = oscillations / (total_variation + np.finfo(float).eps)
            
            # Determine the filter based on OI threshold
            f_j = oi < oi_threshold
            return u, s, vh, f_j
        
        def _deconv(c, U, S, Vh, f_j):
            invS = S ** -1
            invSigma = np.where(invS == np.inf, 0, invS) 
            inv_AIF = np.dot(Vh.T, np.dot(np.diag(f_j * invSigma), U.T))
            k = np.dot(inv_AIF, c)
            return k
        
        self.shift = np.argmax(self.Ca_gamma > 0.01 * np.max(self.Ca_gamma))
        print(f"Shifted {self.shift} frames of the AIF")

        aif = self.Ca_gamma[self.shift:]
        C = np.zeros_like(self.dsc_data)[:,:,:,self.offset:]
        C[self.brain_mask_data] = self.C
        C = C[:,:,:,self.shift:]

        if mode == "svd":
            u, s, v = _svd(aif)
            f_j = np.ones_like(s)
        elif mode == "tsvd":
            u, s, v = _svd(aif)
            f_j = s > (0.2 * s[0])
        elif mode == "tikhonov":
            u, s, v = _svd(aif)
            f_j = (s ** 2) / (s ** 2 + (0.2 * s[0]) ** 2)
        elif mode == "osvd":
            u, s, v, f_j = _osvd(aif)
        else: 
            raise Exception(f"Mode must be chosen between 'svd', 'tsvd', 'tikhonov', or 'osvd', but found {mode}.")

        self.TRF = np.zeros_like(C)
        non_zero_indices = np.nonzero(self.brain_mask_data)
        print(f"Performing {mode} deconvolution...")
        for (i, j, k) in tzip(*non_zero_indices):
            self.TRF[i, j, k, :] = _deconv(C[i, j, k, :], u, s, v, f_j)

        self.TRF_ = self.TRF[self.brain_mask_data]

    def save_image(self, volume, suffix):
        output_path = self.dsc_path.replace(".nii", f"_{suffix}.nii")
        nib.save(
            nib.Nifti1Image(
                volume, self.affine
            ),
            output_path
        )
        return output_path

def single_deconvolution(C, Ca, mode="svd"):
    temp = np.array([np.roll(Ca, i) for i in range(Ca.shape[0])]).T
    Lambda = np.tril(temp)
    u, s, vh = np.linalg.svd(Lambda)
    if mode == "svd":
        f_j = np.ones_like(s)
    elif mode == "tsvd":
        f_j = s > (0.2 * s[0])
    elif mode == "tikhonov":
        f_j = (s ** 2) / (s ** 2 + (0.2 * s[0]) ** 2)
    else: 
        raise Exception(f"Mode parameter must be chosen between 'svd', 'tsvd' or 'tikhonov', but found {mode}.")
    invS = s ** -1
    invSigma = np.where(invS == np.inf, 0, invS) 
    inv_Ca = np.dot(vh.T, np.dot(np.diag(f_j * invSigma), u.T))
    k = np.dot(inv_Ca, C)
    return k
