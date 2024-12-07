import numpy as np
from scipy import stats

# 1. IAAFT Method
import numpy as np

def iaaft(signal, n_iterations=1000, num_surrogates=1):
    """
    IAAFT surrogate generation method.
    Args:
        signal (array-like): Original time series.
        n_iterations (int): Number of iterations to perform.
        num_surrogates (int): Number of surrogate time series to generate.
    Returns:
        list: List of surrogate time series.
    """
    # Input validation
    signal = np.asarray(signal)
    if signal.ndim != 1:
        raise ValueError("Input signal must be one-dimensional")
    if n_iterations < 1:
        raise ValueError("Number of iterations must be positive")
    if num_surrogates < 1:
        raise ValueError("Number of surrogates must be positive")
        
    surrogates = []
    for _ in range(num_surrogates):
        original_spectrum = np.fft.fft(signal)
        sorted_signal = np.sort(signal)
        surrogate = np.random.permutation(signal)

        for _ in range(n_iterations):
            phase_adjusted = np.fft.ifft(original_spectrum * np.exp(1j * np.angle(np.fft.fft(surrogate))))
            surrogate = np.real(phase_adjusted)
            surrogate = sorted_signal[np.argsort(np.argsort(surrogate))]
        
        surrogates.append(surrogate)
    return surrogates

# 2. Enhanced IAAFT Method (IAAFT+)

def iaaft_plus(signal, n_iterations=2000, num_surrogates=1):
    """
    Enhanced IAAFT (IAAFT+) surrogate generation method.
    Args:
        signal (array-like): Original time series.
        n_iterations (int): Number of iterations to perform.
        num_surrogates (int): Number of surrogate time series to generate.
    Returns:
        list: List of surrogate time series.
    """
    # Input validation
    signal = np.asarray(signal)
    if signal.ndim != 1:
        raise ValueError("Input signal must be one-dimensional")
    if n_iterations < 1:
        raise ValueError("Number of iterations must be positive")
    if num_surrogates < 1:
        raise ValueError("Number of surrogates must be positive")
    
    surrogates = []
    for _ in range(num_surrogates):
        original_spectrum = np.fft.fft(signal)
        sorted_signal = np.sort(signal)
        surrogate = np.random.permutation(signal)

        for _ in range(n_iterations):
            phase_adjusted = np.fft.ifft(original_spectrum * np.exp(1j * np.angle(np.fft.fft(surrogate))))
            surrogate = np.real(phase_adjusted)
            surrogate = sorted_signal[np.argsort(np.argsort(surrogate))]
            # Additional enhancement iteration
            original_spectrum = np.fft.fft(surrogate)
        
        surrogates.append(surrogate)
    return surrogates

# 3. IPFT Method

def ipft(signal, n_iterations=1000, num_surrogates=1):
    """
    Iteratively Phase Adjusted Fourier Transform method.
    Args:
        signal (array-like): Original time series.
        n_iterations (int): Number of iterations to perform.
        num_surrogates (int): Number of surrogate time series to generate.
    Returns:
        list: List of surrogate time series.
    """
    surrogates = []
    for _ in range(num_surrogates):
        original_spectrum = np.fft.fft(signal)
        surrogate = np.random.permutation(signal)
        
        for _ in range(n_iterations):
            phase_adjusted = np.fft.ifft(original_spectrum * np.exp(1j * np.angle(np.fft.fft(surrogate))))
            surrogate = np.real(phase_adjusted)
        
        surrogates.append(surrogate)
    return surrogates

# 4. ISAAFT Method

def isaaft(signal, n_iterations=1000, num_surrogates=1):
    """
    Iteratively Shifted Amplitude Adjusted Fourier Transform method.
    Args:
        signal (array-like): Original time series.
        n_iterations (int): Number of iterations to perform.
        num_surrogates (int): Number of surrogate time series to generate.
    Returns:
        list: List of surrogate time series.
    """
    signal = np.asarray(signal)
    if len(signal) < 2:
        raise ValueError("Signal length must be at least 2")
    
    surrogates = []
    for _ in range(num_surrogates):
        original_spectrum = np.fft.rfft(signal)  # Use rfft for better efficiency
        sorted_signal = np.sort(signal)
        surrogate = np.random.permutation(signal)
        
        for _ in range(n_iterations):
            # Correct spectrum shift operation
            shift_amount = np.random.randint(1, len(original_spectrum))  # Avoid zero shift
            shifted_spectrum = np.roll(original_spectrum, shift_amount)
            phase_adjusted = np.fft.irfft(shifted_spectrum * 
                                        np.exp(1j * np.angle(np.fft.rfft(surrogate))),
                                        n=len(signal))
            surrogate = sorted_signal[np.argsort(np.argsort(np.real(phase_adjusted)))]
        
        surrogates.append(surrogate)
    return surrogates

# 5. AIAAFT Method

def aiaaft(signal, n_iterations=1000, num_surrogates=1, adaptation_range=0.05):
    """
    Adaptive Iteratively Amplitude Adjusted Fourier Transform method.
    Args:
        signal (array-like): Original time series.
        n_iterations (int): Number of iterations to perform.
        num_surrogates (int): Number of surrogate time series to generate.
        adaptation_range (float): Range for adaptive spectrum modification (default: 0.05)
    Returns:
        list: List of surrogate time series.
    """
    surrogates = []
    for _ in range(num_surrogates):
        original_spectrum = np.fft.fft(signal)
        sorted_signal = np.sort(signal)
        surrogate = np.random.permutation(signal)

        for iter in range(n_iterations):
            # Dynamically adjust adaptation range
            current_range = adaptation_range * (1 - iter/n_iterations)
            adaptive_spectrum = original_spectrum * (1 + np.random.uniform(
                -current_range, current_range, len(original_spectrum)))
            phase_adjusted = np.fft.ifft(adaptive_spectrum * np.exp(1j * np.angle(np.fft.fft(surrogate))))
            surrogate = np.real(phase_adjusted)
            surrogate = sorted_signal[np.argsort(np.argsort(surrogate))]
        
        surrogates.append(surrogate)
    return surrogates

# 6. IAAWT Method

def dwt(signal, level=1):
    signal = np.asarray(signal)
    if len(signal) < 2:
        raise ValueError("Signal length must be at least 2")
    
    result = []
    current = signal.copy()
    
    for _ in range(level):
        n = len(current)
        if n < 2:
            break
            
        # Ensure even length
        if n % 2:
            current = np.pad(current, (0, 1), mode='reflect')
            n += 1
            
        h = current.reshape(-1, 2)
        approx = (h[:, 0] + h[:, 1]) / np.sqrt(2)
        detail = (h[:, 0] - h[:, 1]) / np.sqrt(2)
        
        result.append(detail)
        current = approx
    
    result.append(current)
    return result[::-1]

def idwt(coeffs):
    """
    Simple implementation of inverse discrete wavelet transform
    
    Args:
        coeffs: List of wavelet coefficients
    
    Returns:
        array: Reconstructed signal
    """
    current = coeffs[0]
    
    for detail in coeffs[1:]:
        n = len(current)
        # Reconstruct signal
        reconstructed = np.zeros(2 * n)
        reconstructed[::2] = (current + detail) / np.sqrt(2)
        reconstructed[1::2] = (current - detail) / np.sqrt(2)
        current = reconstructed
    
    return current

def iaawt(signal, n_iterations=1000, num_surrogates=1, level=None):
    """
    Generate surrogates using the Iterative Amplitude Adjusted Wavelet Transform (IAAWT) method.
    Uses a simple Haar wavelet implementation with numpy.
    
    Parameters
    ----------
    signal : array-like
        Input time series (1D array)
    n_iterations : int, optional
        Number of iterations (default: 1000)
    num_surrogates : int, optional
        Number of surrogate time series to generate (default: 1)
    level : int, optional
        Decomposition level. If None, it will be automatically determined
        based on the signal length.
        
    Returns
    -------
    list
        List of surrogate time series
    """
    # Input validation
    signal = np.asarray(signal)
    if signal.ndim != 1:
        raise ValueError("Input signal must be one-dimensional")
    if n_iterations < 1:
        raise ValueError("Number of iterations must be positive")
    if num_surrogates < 1:
        raise ValueError("Number of surrogates must be positive")
    
    # Determine decomposition level if not specified
    if level is None:
        level = int(np.log2(len(signal))) - 1
    
    surrogates = []
    signal_length = len(signal)
    sorted_signal = np.sort(signal)
    
    # Get original wavelet coefficients
    coeffs_orig = dwt(signal, level=level)
    
    for _ in range(num_surrogates):
        # Initialize with random permutation
        surrogate = np.random.permutation(signal)
        
        for _ in range(n_iterations):
            # Wavelet decomposition of surrogate
            coeffs = dwt(surrogate, level=level)
            
            # Adjust coefficients
            new_coeffs = []
            for orig_c, curr_c in zip(coeffs_orig, coeffs):
                # Preserve amplitudes of original, but use phases of surrogate
                amp_orig = np.abs(orig_c)
                phases = np.angle(curr_c + 1j * np.finfo(float).eps)  # Add small constant to avoid division by zero
                new_c = amp_orig * np.exp(1j * phases)
                new_coeffs.append(new_c.real)
            
            # Inverse wavelet transform
            surrogate_temp = idwt(new_coeffs)
            
            # Amplitude adjustment
            if len(surrogate_temp) > signal_length:
                surrogate_temp = surrogate_temp[:signal_length]
            ranks = np.argsort(np.argsort(surrogate_temp))
            surrogate = sorted_signal[ranks]
        
        surrogates.append(surrogate)
    
    return surrogates

# 7. Shuffle Surrogate Method

def shuffle_surrogate(signal, num_surrogates=1, preserve_distribution=True):
    """
    Generate surrogates using the Shuffle Surrogate method by randomly permuting the original time series.
    
    Parameters
    ----------
    signal : array-like
        Input time series (1D array)
    num_surrogates : int, optional
        Number of surrogate time series to generate (default: 1)
    preserve_distribution : bool, optional
        If True, ensures exact preservation of the original amplitude distribution.
        If False, allows for small variations due to random sampling (default: True)
        
    Returns
    -------
    list
        List of surrogate time series
    
    Notes
    -----
    This method completely destroys both linear and nonlinear correlations while
    preserving the amplitude distribution of the original signal.
    """
    # Input validation
    signal = np.asarray(signal)
    if signal.ndim != 1:
        raise ValueError("Input signal must be one-dimensional")
    if num_surrogates < 1:
        raise ValueError("Number of surrogates must be positive")
    
    surrogates = []
    
    if preserve_distribution:
        # Generate surrogates using permutation
        for _ in range(num_surrogates):
            surrogate = np.random.permutation(signal)
            surrogates.append(surrogate)
    else:
        # Generate surrogates using bootstrap resampling
        signal_length = len(signal)
        for _ in range(num_surrogates):
            indices = np.random.randint(0, signal_length, size=signal_length)
            surrogate = signal[indices]
            surrogates.append(surrogate)
    
    return surrogates

# 8. MBB Surrogate Method

def mbb_surrogate(signal, block_length=None, num_surrogates=1, overlap=True):
    """
    Generate surrogates using the Moving Block Bootstrap method.
    
    Parameters
    ----------
    signal : array-like
        Input time series (1D array)
    block_length : int, optional
        Length of blocks to use. If None, will be automatically determined
        as sqrt(signal length) rounded to nearest integer.
    num_surrogates : int, optional
        Number of surrogate time series to generate (default: 1)
    overlap : bool, optional
        Whether to use overlapping blocks (default: True)
        
    Returns
    -------
    list
        List of surrogate time series
    
    Notes
    -----
    This method preserves the local temporal structure within blocks while
    randomizing the relationships between blocks. The block_length parameter
    controls the trade-off between preserving local structure (larger blocks)
    and maintaining variability (smaller blocks).
    """
    # Input validation
    signal = np.asarray(signal)
    if signal.ndim != 1:
        raise ValueError("Input signal must be one-dimensional")
    if num_surrogates < 1:
        raise ValueError("Number of surrogates must be positive")
    
    signal_length = len(signal)
    
    # Determine block length if not specified
    if block_length is None:
        block_length = int(np.sqrt(signal_length))
    elif block_length < 1:
        raise ValueError("Block length must be positive")
    elif block_length > signal_length:
        raise ValueError("Block length cannot be larger than signal length")
    
    surrogates = []
    
    # Calculate number of blocks needed
    if overlap:
        # For overlapping blocks
        available_blocks = signal_length - block_length + 1
        blocks_needed = int(np.ceil(signal_length / block_length))
    else:
        # For non-overlapping blocks
        available_blocks = signal_length // block_length
        blocks_needed = available_blocks
    
    for _ in range(num_surrogates):
        surrogate = np.zeros(signal_length)
        current_position = 0
        
        # Generate surrogate by concatenating random blocks
        while current_position < signal_length:
            # Randomly select block start position
            if overlap:
                block_start = np.random.randint(0, signal_length - block_length + 1)
            else:
                block_start = np.random.randint(0, available_blocks) * block_length
            
            # Extract block
            block = signal[block_start:block_start + block_length]
            
            # Add block to surrogate
            end_position = min(current_position + block_length, signal_length)
            block_portion = end_position - current_position
            surrogate[current_position:end_position] = block[:block_portion]
            
            current_position = end_position
        
        surrogates.append(surrogate)
    
    return surrogates

# 9. Phase Randomization Method

def phase_randomization(signal, num_surrogates=1, preserve_symmetry=True):
    """
    Generate surrogates using the Phase Randomization method.
    
    Parameters
    ----------
    signal : array-like
        Input time series (1D array)
    num_surrogates : int, optional
        Number of surrogate time series to generate (default: 1)
    preserve_symmetry : bool, optional
        If True, ensures that the phase randomization preserves
        the Hermitian symmetry of the Fourier transform for real signals
        (default: True)
        
    Returns
    -------
    list
        List of surrogate time series
    
    Notes
    -----
    This method preserves the linear correlation structure (power spectrum) 
    while destroying nonlinear dependencies by randomizing the Fourier phases.
    The amplitude spectrum of the original signal is exactly preserved.
    """
    # Input validation
    signal = np.asarray(signal)
    if signal.ndim != 1:
        raise ValueError("Input signal must be one-dimensional")
    if num_surrogates < 1:
        raise ValueError("Number of surrogates must be positive")
    
    signal_length = len(signal)
    surrogates = []
    
    # Get original Fourier transform
    fft_signal = np.fft.fft(signal)
    amplitudes = np.abs(fft_signal)
    
    # Generate surrogates
    for _ in range(num_surrogates):
        if preserve_symmetry:
            # Generate random phases preserving Hermitian symmetry
            random_phases = np.random.uniform(0, 2*np.pi, size=(signal_length // 2 + 1))
            phases = np.zeros(signal_length)
            phases[0] = 0  # DC component remains unchanged
            phases[1:signal_length//2 + 1] = random_phases[1:]
            phases[signal_length//2 + 1:] = -random_phases[1:signal_length//2][::-1]
            
            # Special handling for even-length signals
            if signal_length % 2 == 0:
                phases[signal_length//2] = 0  # Nyquist frequency component remains real
        else:
            # Simple random phases without symmetry constraint
            phases = np.random.uniform(0, 2*np.pi, size=signal_length)
            phases[0] = 0  # Keep DC component real
        
        # Generate surrogate in frequency domain
        surrogate_fft = amplitudes * np.exp(1j * phases)
        
        # Transform back to time domain
        surrogate = np.real(np.fft.ifft(surrogate_fft))
        
        surrogates.append(surrogate)
    return surrogates

# Multivariate IAAFT Surrogate Method
def multivariate_iaaft(data, max_iter=100, num_surrogates=1, tol=1e-6):
    data = np.asarray(data)
    if data.ndim != 2:
        raise ValueError("Input data must be two-dimensional")
    
    n_samples, n_vars = data.shape
    surrogates = []
    
    for _ in range(num_surrogates):
        surrogate = np.zeros_like(data)
        for j in range(n_vars):
            surrogate[:, j] = np.random.permutation(data[:, j])
        
        orig_sort = np.sort(data, axis=0)
        orig_fft = np.fft.rfft(data, axis=0)
        
        prev_surrogate = np.inf
        for iter in range(max_iter):
            # Spectral adjustment
            for j in range(n_vars):
                fft_surrogate = np.fft.rfft(surrogate[:, j])
                phases = np.angle(fft_surrogate)
                surrogate[:, j] = np.real(np.fft.irfft(
                    np.abs(orig_fft[:, j]) * np.exp(1j * phases),
                    n=n_samples
                ))
            
            # Amplitude adjustment
            for j in range(n_vars):
                rank = np.argsort(np.argsort(surrogate[:, j]))
                surrogate[:, j] = orig_sort[rank, j]
            
            # More robust convergence check
            diff = np.abs(surrogate - prev_surrogate)
            if np.mean(diff) < tol and np.max(diff) < tol * 10:
                break
            prev_surrogate = surrogate.copy()
        
        surrogates.append(surrogate.copy())
    
    return surrogates

def copula_surrogate(data, num_surrogates=1, copula_type='gaussian'):
    """
    Generate multivariate surrogate data using Copula method
    
    Args:
        data: Original data, shape (N, d), where N is sample size, d is dimension
        num_surrogates: Number of surrogate data to generate
        copula_type: Type of copula ('gaussian' or 't')
    
    Returns:
        Generated surrogate data, shape (num_surrogates, N, d)
    """
    N, d = data.shape
    surrogate_data = np.zeros((num_surrogates, N, d))
    
    # Step 1: Calculate empirical distribution function for each variable
    U = np.zeros_like(data, dtype=float)
    sorted_data = np.zeros_like(data)
    for i in range(d):
        ranks = np.argsort(data[:, i])
        U[:, i] = (ranks + 1) / (N + 1)  # Use (n+1) to avoid 1
        sorted_data[:, i] = np.sort(data[:, i])
    
    # Step 2: Estimate Copula parameters
    # Convert U to standard normal distribution
    Z = stats.norm.ppf(U)
    # Calculate correlation matrix
    corr = np.corrcoef(Z.T)
    
    # Step 3: Generate new samples
    for k in range(num_surrogates):
        if copula_type == 'gaussian':
            # Generate multivariate normal distribution samples
            Z_new = np.random.multivariate_normal(
                mean=np.zeros(d),
                cov=corr,
                size=N
            )
        else:  # t-copula
            # Generate multivariate t distribution samples
            df = 4  # Degrees of freedom
            Z_new = np.random.multivariate_normal(
                mean=np.zeros(d),
                cov=corr,
                size=N
            ) * np.sqrt(df / np.random.chisquare(df, size=(N, 1)))
        
        # Convert back to uniform distribution
        U_new = stats.norm.cdf(Z_new)
        
        # Step 4: Inverse transform sampling
        for i in range(d):
            # Handle boundary cases
            U_new[:, i] = np.clip(U_new[:, i], 1e-10, 1-1e-10)
            ranks = np.floor(U_new[:, i] * (N - 1)).astype(int)
            ranks_next = np.minimum(ranks + 1, N - 1)
            frac = (U_new[:, i] * (N - 1)) - ranks
            
            surrogate_data[k, :, i] = (1 - frac) * sorted_data[ranks, i] + \
                                    frac * sorted_data[ranks_next, i]
    
    # If only generating one surrogate, remove the first dimension
    if num_surrogates == 1:
        surrogate_data = surrogate_data[0]
    
    return surrogate_data

# Block Bootstrap Method Extension
def block_bootstrap(data, block_length, num_bootstrap=1000):
    """
    Block Bootstrap method
    
    Args:
        data: Time series data
        block_length: Length of blocks
        num_bootstrap: Number of bootstrap samples
    
    Returns:
        list: List of bootstrap samples
    """
    data = np.asarray(data)
    n = len(data)
    
    # Calculate required number of blocks
    num_blocks = int(np.ceil(n / block_length))
    
    # Generate Bootstrap samples
    bootstrap_samples = []
    for _ in range(num_bootstrap):
        # Randomly select block start positions
        start_indices = np.random.randint(0, n - block_length + 1, size=num_blocks)
        
        # Build Bootstrap sample
        sample = []
        for start in start_indices:
            block = data[start:start + block_length]
            sample.extend(block)
        
        # Truncate to original length
        sample = sample[:n]
        bootstrap_samples.append(np.array(sample))
    
    return bootstrap_samples

def stationary_bootstrap(data, mean_block_length, num_bootstrap=1000):
    """
    Stationary Bootstrap method
    
    Args:
        data: Time series data
        mean_block_length: Average block length
        num_bootstrap: Number of bootstrap samples
    
    Returns:
        list: List of bootstrap samples
    """
    data = np.asarray(data)
    n = len(data)
    p = 1 / mean_block_length  # Probability of starting new block
    
    bootstrap_samples = []
    for _ in range(num_bootstrap):
        sample = []
        while len(sample) < n:
            # Randomly select start position
            start = np.random.randint(0, n)
            current = start
            
            # Generate block with geometric distribution length
            while len(sample) < n and np.random.random() > p:
                sample.append(data[current])
                current = (current + 1) % n
        
        # Truncate to original length
        sample = sample[:n]
        bootstrap_samples.append(np.array(sample))
    
    return bootstrap_samples

def mvts_surrogate_pca(data, num_surrogates=1, n_components=None):
    """
    Generate multivariate time series surrogate data using PCA decomposition
    
    Args:
        data: Original data, shape (N, d), where N is sample size, d is dimension
        num_surrogates: Number of surrogate data to generate
        n_components: Number of PCA components to retain, None means keep all
    
    Returns:
        Generated surrogate data, shape (num_surrogates, N, d)
    """
    N, d = data.shape
    surrogate_data = np.zeros((num_surrogates, N, d))
    
    # Data normalization
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    data_normalized = (data - mean) / std
    
    # PCA decomposition
    U, S, Vt = np.linalg.svd(data_normalized, full_matrices=False)
    if n_components is None:
        n_components = d
    
    # Generate surrogate data
    for k in range(num_surrogates):
        # Generate surrogate data for each principal component
        surrogate_components = np.zeros_like(U)
        for i in range(n_components):
            component = U[:, i]
            # Use IAAFT method to generate surrogate data
            surrogate = iaaft(component, n_iterations=100, num_surrogates=1)[0]
            surrogate_components[:, i] = surrogate
        
        # Reconstruct data
        surrogate_normalized = surrogate_components @ np.diag(S) @ Vt
        surrogate_data[k] = surrogate_normalized * std + mean
    
    if num_surrogates == 1:
        surrogate_data = surrogate_data[0]
    
    return surrogate_data

def mvts_surrogate_wavelet(data, num_surrogates=1, level=None):
    N, d = data.shape
    if level is None:
        level = int(np.log2(N))
    level = min(level, int(np.log2(N)))  # Ensure not exceeding maximum possible levels
    
    surrogate_data = np.zeros((num_surrogates, N, d))
    
    for k in range(num_surrogates):
        surrogate = np.zeros_like(data)
        for i in range(d):
            try:
                coeffs = dwt(data[:, i], level=level)
                surrogate_coeffs = []
                for j, coef in enumerate(coeffs):
                    if j == 0:
                        surrogate_coeffs.append(coef)
                    else:
                        surrogate_coef = iaaft(coef, n_iterations=100, num_surrogates=1)[0]
                        surrogate_coeffs.append(surrogate_coef)
                
                surrogate[:, i] = idwt(surrogate_coeffs)
                sorted_orig = np.sort(data[:, i])
                surrogate[:, i] = sorted_orig[np.argsort(np.argsort(surrogate[:, i]))]
            except Exception as e:
                print(f"Warning: Error processing dimension {i}: {str(e)}")
                surrogate[:, i] = data[:, i]  # Use original data as fallback
        
        surrogate_data[k] = surrogate
    
    return surrogate_data[0] if num_surrogates == 1 else surrogate_data

def s_transform(signal, fs=1.0):
    N = len(signal)
    freqs = np.fft.fftfreq(N, 1/fs)
    signal_freq = np.fft.fft(signal)
    
    st = np.zeros((N, N), dtype=complex)
    for idx, freq in enumerate(freqs):
        if freq == 0:
            st[idx, :] = np.mean(signal)
            continue
        
        sigma = 1.0 / abs(freq)
        gauss = np.exp(-2 * (np.pi ** 2) * (sigma ** 2) * 
                      ((np.arange(N) - N/2) ** 2) / N)
        st[idx, :] = np.fft.ifft(signal_freq * gauss)
    
    return st

def inverse_s_transform(st):
    if not np.iscomplexobj(st):
        raise ValueError("Input must be complex-valued")
    return np.real(np.mean(st, axis=0))

def mvts_surrogate_s_transform(data, num_surrogates=1, preserve_scale=True):
    """
    Generate multivariate time series surrogate data using S-transform and IAAFT method
    
    Args:
        data: Original data, shape (N, d), N is sample size, d is dimension
        num_surrogates: Number of surrogate data to generate
        preserve_scale: Whether to preserve time scale characteristics
    
    Returns:
        Generated surrogate data, shape (num_surrogates, N, d)
    """
    N, d = data.shape
    surrogate_data = np.zeros((num_surrogates, N, d))
    
    for k in range(num_surrogates):
        surrogate = np.zeros_like(data)
        
        for i in range(d):
            # Calculate S-transform
            st = s_transform(data[:, i])
            
            if preserve_scale:
                # Preserve time scale characteristics, only randomize phases
                magnitude = np.abs(st)
                phase = np.angle(st)
                random_phase = np.random.uniform(0, 2*np.pi, phase.shape)
                if i > 0:  # Keep phase relationship for dimensions after the first
                    # More robust phase difference handling
                    phase_diff_i = np.angle(np.exp(1j * (phase_diff[i] + np.pi))) - np.pi
                    random_phase = phase + phase_diff_i
                new_st = magnitude * np.exp(1j * random_phase)
                
                if i == 0:  # Record phase difference for the first dimension
                    phase_diff = random_phase - phase
            else:
                # Use IAAFT method on S-transform results
                for freq_idx in range(N):
                    st[freq_idx, :] = iaaft(np.real(st[freq_idx, :]), 
                                          n_iterations=100, 
                                          num_surrogates=1)[0]
                new_st = st
            
            # Inverse S-transform to reconstruct time series
            surrogate[:, i] = inverse_s_transform(new_st)
            
            # Adjust amplitude distribution to match the original data
            sorted_orig = np.sort(data[:, i])
            surrogate[:, i] = sorted_orig[np.argsort(np.argsort(surrogate[:, i]))]
        
        surrogate_data[k] = surrogate
    
    if num_surrogates == 1:
        surrogate_data = surrogate_data[0]
    
    return surrogate_data

