import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from utils.lb import lb
from statsmodels.tsa.stattools import adfuller
from utils.trend import decompose
from utils.skew import skew
from utils.kurtosis import kurtosis
from utils.acf import acf
from scipy.signal import welch
from scipy.signal import periodogram
import re
from scipy import stats

def get_stars(pvalue):
    if pvalue <= 0.01:
        return '***'
    elif pvalue <= 0.05:
        return '**'
    elif pvalue <= 0.1:
        return '*'
    return ''

def calculate_stats(ts, lb_lags=10, adf_regression='c'):
    """
    Calculate statistical measures of a time series
    Args:
        ts: Time series data
        lb_lags: Ljung-Box test lag order
        adf_regression: ADF test regression type ('c' constant term, 'ct' constant and trend term, 'n' no constant or trend term)
    """
    # Convert input to numpy array
    if isinstance(ts, pd.Series):
        ts_array = ts.values
    else:
        ts_array = np.asarray(ts)
    
    mean = np.mean(ts_array)
    std = np.std(ts_array)
    skew_value = skew(ts_array)
    kurt_value = kurtosis(ts_array)
    
    # Ljung-Box test
    lb_stat, lb_pvalue = lb(ts_array, lb_lags)
    
    # ADF test
    adf_result = adfuller(ts_array, regression=adf_regression)
    adf_stat = adf_result[0]
    adf_pvalue = adf_result[1]
    
    return {
        'Mean': f"{mean:.4f}",
        'Std Dev': f"{std:.4f}",
        'Skewness': f"{skew_value:.4f}",
        'Kurtosis': f"{kurt_value:.4f}",
        f'LB({lb_lags})': f"{lb_stat:.4f}{get_stars(lb_pvalue)}",
        f'ADF({adf_regression})': f"{adf_stat:.4f}{get_stars(adf_pvalue)}"
    }

def _convert_to_series(data):
    """Convert different input formats to pandas.Series
    
    Supported input formats:
    - pandas.Series
    - pandas.DataFrame's one column
    - numpy.ndarray
    - list
    - dict's values
    """
    if isinstance(data, pd.Series):
        return data
    elif isinstance(data, pd.DataFrame):
        if data.shape[1] == 1:
            return data.iloc[:, 0]
        else:
            raise ValueError("DataFrame must have only one column")
    elif isinstance(data, (np.ndarray, list)):
        return pd.Series(data)
    else:
        raise TypeError("Unsupported data type. Please provide pandas.Series, single-column DataFrame, numpy.ndarray, or list")

def _process_input_data(data):
    """Process input data and convert to standard format
    
    Args:
        data: Can be one of the following formats:
            - dict: {name: series, ...}
            - pandas.DataFrame: Each column as a sequence
            - pandas.Series: Single sequence
            - numpy.ndarray: If it's a 1D array, it's treated as a single sequence; if it's a 2D array, each column is treated as a sequence
            - list: Treated as a single sequence
    
    Returns:
        dict: {name: pandas.Series, ...}
    """
    if isinstance(data, dict):
        return {name: _convert_to_series(series) for name, series in data.items()}
    elif isinstance(data, pd.DataFrame):
        return {col: data[col] for col in data.columns}
    elif isinstance(data, pd.Series):
        return {'Series': data}
    elif isinstance(data, np.ndarray):
        if data.ndim == 1:
            return {'Series': pd.Series(data)}
        elif data.ndim == 2:
            return {f'Series_{i}': pd.Series(data[:, i]) for i in range(data.shape[1])}
    elif isinstance(data, list):
        return {'Series': pd.Series(data)}
    else:
        raise TypeError("Unsupported data type")

def ts_statistics(data, save_path=False, lb_lags=10, adf_regression='c'):
    """
    Calculate descriptive statistics table of time series
    
    Args:
        data: Can be one of the following formats:
            - dict: {name: series, ...}
            - pandas.DataFrame: Each column as a sequence
            - pandas.Series: Single sequence
            - numpy.ndarray: 1D or 2D array
            - list: Single sequence
        save_path: False means not to save, True means save in the current directory, and a string means save in the specified path
        lb_lags: Ljung-Box test lag order
        adf_regression: ADF test regression type
    
    Returns:
        pandas.DataFrame: DataFrame containing statistical results
    """
    # Convert input data to standard format
    series_dict = _process_input_data(data)
    
    results = {}
    for name, ts in series_dict.items():
        results[name] = calculate_stats(ts, lb_lags=lb_lags, adf_regression=adf_regression)
    
    stats_df = pd.DataFrame(results).T
    
    # Handle saving logic
    if save_path:
        path = '.' if save_path is True else save_path
        stats_df.to_csv(f"{path}/time_series_statistics.csv")
    
    return stats_df

def plot_decomposition(data, lag=10, period=12, save_path=False, dpi=None):
    """
    Plot decomposition for each time series
    
    Args:
        data: Can be one of the following formats:
            - dict: {name: series, ...}
            - pandas.DataFrame: Each column as a sequence
            - pandas.Series: Single sequence
            - numpy.ndarray: 1D or 2D array
            - list: Single sequence
        lag: Autocorrelation lag order
        period: Seasonal period
        save_path: False means not to save, True means save in the current directory, and a string means save in the specified path
        dpi: DPI value for saving images, only effective when save_path is not False
    """
    # Convert input data to standard format
    series_dict = _process_input_data(data)
    
    for name, ts in series_dict.items():
        print(f"\n{name}:")
        
        # Convert Series to numpy array
        ts_array = ts.values if isinstance(ts, pd.Series) else np.asarray(ts)
        
        # Decomposition
        decomposition = decompose(ts_array, period)
        trend = decomposition['trend']
        seasonal = decomposition['seasonal']
        residual = decomposition['resid']
        
        print(f"Trend component mean: {np.mean(trend[~np.isnan(trend)]):.4f}")
        print(f"Seasonal component amplitude: {np.ptp(seasonal[~np.isnan(seasonal)]):.4f}")
        
        # Autocorrelation
        acf_value = acf(ts_array, lag)
        print("Autocorrelations up to lag 10:")
        print([f"{x:.4f}" for x in acf_value[1:]])
        
        # Plot decomposition
        plt.figure(figsize=(12, 8))
        plt.subplot(411)
        plt.plot(ts)
        plt.title(f'{name} - Original')
        plt.subplot(412)
        plt.plot(trend)
        plt.title('Trend')
        plt.subplot(413)
        plt.plot(seasonal)
        plt.title('Seasonal')
        plt.subplot(414)
        plt.plot(residual)
        plt.title('Residual')
        plt.tight_layout()
        
        # Handle saving logic
        if save_path:
            # If save_path is True, use the current directory
            path = '.' if save_path is True else save_path
            save_params = {}
            if dpi is not None:
                save_params['dpi'] = dpi
            plt.savefig(f"{path}/{name}_decomposition.png", **save_params)
        
        plt.show()

# Time series preprocessing module
def interpolate_missing(ts, method='linear'):
    """
    Handle missing values in time series
    
    Args:
        ts: Time series data (pandas.Series or numpy.ndarray)
        method: Interpolation method ('linear', 'ffill', 'bfill', 'cubic', 'spline')
    
    Returns:
        Interpolated time series
    """
    if isinstance(ts, np.ndarray):
        ts = pd.Series(ts)
    
    if method in ['linear', 'ffill', 'bfill']:
        return ts.interpolate(method=method)
    elif method == 'cubic':
        return ts.interpolate(method='cubic')
    elif method == 'spline':
        return ts.interpolate(method='spline', order=3)
    else:
        raise ValueError("Unsupported interpolation method")

def detect_outliers(ts, method='zscore', threshold=3):
    """
    Detect outliers in time series
    
    Args:
        ts: Time series data
        method: Detection method ('zscore', 'iqr', 'mad')
        threshold: Value
    
    Returns:
        Boolean index of outliers
    """
    ts_array = np.asarray(ts)
    
    if method == 'zscore':
        z_scores = np.abs((ts_array - np.mean(ts_array)) / np.std(ts_array))
        return z_scores > threshold
    elif method == 'iqr':
        q1, q3 = np.percentile(ts_array, [25, 75])
        iqr = q3 - q1
        return (ts_array < (q1 - threshold * iqr)) | (ts_array > (q3 + threshold * iqr))
    elif method == 'mad':
        median = np.median(ts_array)
        mad = np.median(np.abs(ts_array - median))
        return np.abs(ts_array - median) > threshold * mad
    else:
        raise ValueError("Unsupported outlier detection method")

def normalize_ts(ts, method='zscore'):
    """
    Time series normalization
    
    Args:
        ts: Time series data
        method: Normalization method ('zscore', 'minmax', 'robust')
    
    Returns:
        Normalized time series
    """
    ts_array = np.asarray(ts)
    
    if method == 'zscore':
        return (ts_array - np.mean(ts_array)) / np.std(ts_array)
    elif method == 'minmax':
        return (ts_array - np.min(ts_array)) / (np.max(ts_array) - np.min(ts_array))
    elif method == 'robust':
        median = np.median(ts_array)
        q1, q3 = np.percentile(ts_array, [25, 75])
        return (ts_array - median) / (q3 - q1)
    else:
        raise ValueError("Unsupported normalization method")

def resample_ts(ts, freq, method='mean'):
    """
    Time series resampling
    
    Args:
        ts: Time series data (pandas.Series with DatetimeIndex)
        freq: Resampling frequency ('D', 'W', 'M', 'Q', 'Y')
        method: Aggregation method ('mean', 'sum', 'first', 'last', 'max', 'min')
    
    Returns:
        Resampled time series
    """
    if not isinstance(ts, pd.Series):
        raise ValueError("Input must be a pandas Series with DatetimeIndex")
    
    return getattr(ts.resample(freq), method)()

# Feature extraction module
def extract_time_features(ts):
    """
    Extract time domain features of a time series
    
    Args:
        ts: Time series data
    
    Returns:
        Dictionary containing time domain features
    """
    ts_array = np.asarray(ts)
    
    return {
        'mean': np.mean(ts_array),
        'std': np.std(ts_array),
        'skewness': skew(ts_array),
        'kurtosis': kurtosis(ts_array),
        'max': np.max(ts_array),
        'min': np.min(ts_array),
        'range': np.ptp(ts_array),
        'median': np.median(ts_array),
        'iqr': np.percentile(ts_array, 75) - np.percentile(ts_array, 25)
    }

def extract_freq_features(ts, fs=1.0):
    """
    Extract frequency domain features of a time series
    
    Args:
        ts: Time series data
        fs: Sampling frequency
    
    Returns:
        Dictionary containing frequency domain features
    """
    ts_array = np.asarray(ts)
    
    # Calculate FFT
    fft_vals = np.fft.fft(ts_array)
    fft_freqs = np.fft.fftfreq(len(ts_array), 1/fs)
    
    # Calculate power spectrum
    power_spectrum = np.abs(fft_vals)**2
    
    return {
        'dominant_freq': fft_freqs[np.argmax(power_spectrum[1:]) + 1],
        'spectral_mean': np.mean(power_spectrum),
        'spectral_std': np.std(power_spectrum),
        'spectral_entropy': -np.sum(power_spectrum * np.log2(power_spectrum + 1e-10))
    }

def calculate_entropy(ts, m=2, r=0.2):
    """
    Calculate sample entropy of a time series
    """
    ts_array = np.asarray(ts)
    n = len(ts_array)
    r = r * np.std(ts_array)
    
    def create_templates(m_):
        return np.array([ts_array[i:i+m_] for i in range(n-m_+1)])
    
    def count_matches(templates):
        dist = np.abs(templates[:, np.newaxis] - templates)
        return np.sum(np.all(dist < r, axis=2), axis=1) - 1
    
    templates_m = create_templates(m)
    templates_m1 = create_templates(m+1)
    
    B = np.sum(count_matches(templates_m))
    A = np.sum(count_matches(templates_m1))
    
    B = B / ((n-m+1) * (n-m))
    A = A / ((n-m) * (n-m-1))
    
    return -np.log(A/B) if A > 0 and B > 0 else np.inf

# Causal relationship analysis module
def granger_causality(x, y, max_lag=5, alpha=0.05):
    """
    Perform Granger causality test
    
    Args:
        x: First time series
        y: Second time series
        max_lag: Maximum lag order
        alpha: Significance level
    
    Returns:
        dict: Dictionary containing test results
    """
    from statsmodels.tsa.stattools import grangercausalitytests
    
    x = np.asarray(x)
    y = np.asarray(y)
    data = np.column_stack([y, x])
    
    results = grangercausalitytests(data, maxlag=max_lag, verbose=False)
    
    causality_results = {}
    for lag in range(1, max_lag + 1):
        test_stat = results[lag][0]['ssr_chi2test']
        causality_results[lag] = {
            'test_statistic': test_stat[0],
            'p_value': test_stat[1],
            'significant': test_stat[1] < alpha
        }
    
    return causality_results

def transfer_entropy(x, y, k=1, l=1, bins=10):
    """
    Calculate transfer entropy (improved version)
    """
    x = np.asarray(x)
    y = np.asarray(y)
    
    def get_symbolic_series(series, delay):
        n = len(series)
        result = np.zeros((n, delay))
        for i in range(delay):
            result[delay-1:, i] = series[i:n-delay+1+i]
        return result[delay-1:]
    
    # Build state space
    x_past = get_symbolic_series(x[:-1], k)
    y_past = get_symbolic_series(y[:-1], l)
    y_future = y[k:]
    
    # Use histogram to estimate probability distribution (more stable)
    def estimate_entropy(hist):
        hist = hist / np.sum(hist)
        return -np.sum(hist[hist > 0] * np.log2(hist[hist > 0]))
    
    # Calculate joint and conditional entropy
    joint_hist, _ = np.histogramdd(np.column_stack([y_future, 
                                                   x_past.mean(axis=1),
                                                   y_past.mean(axis=1)]), 
                                 bins=bins)
    marg_hist, _ = np.histogramdd(np.column_stack([y_future,
                                                  y_past.mean(axis=1)]),
                                bins=bins)
    
    h_joint = estimate_entropy(joint_hist)
    h_marg = estimate_entropy(marg_hist)
    
    return h_marg - h_joint

def mutual_information(x, y, bins=10):
    x = np.asarray(x)
    y = np.asarray(y)
    
    if len(x) != len(y):
        raise ValueError("Input arrays must have the same length")
    
    if bins is None:
        bins = int(np.log2(len(x)) + 1)
    
    hist_xy, x_edges, y_edges = np.histogram2d(x, y, bins=bins)
    hist_x = np.histogram(x, bins=x_edges)[0]
    hist_y = np.histogram(y, bins=y_edges)[0]
    
    eps = np.finfo(float).eps
    p_xy = hist_xy / np.sum(hist_xy) + eps
    p_x = hist_x / np.sum(hist_x) + eps
    p_y = hist_y / np.sum(hist_y) + eps
    
    mi = np.sum(p_xy * np.log2(p_xy / (p_x[:, np.newaxis] * p_y[np.newaxis, :])))
    
    return max(0, mi)

def phase_sync_analysis(x, y):
    """
    Calculate phase synchronization of two time series
    
    Args:
        x: First time series
        y: Second time series
    
    Returns:
        Dictionary containing phase synchronization metrics
    """
    from scipy.signal import hilbert
    
    # Calculate analytic signal
    x_analytic = hilbert(x)
    y_analytic = hilbert(y)
    
    # Extract phase
    x_phase = np.angle(x_analytic)
    y_phase = np.angle(y_analytic)
    
    # Calculate phase difference
    phase_diff = x_phase - y_phase
    
    # Calculate phase synchronization metrics
    sync_index = np.abs(np.mean(np.exp(1j * phase_diff)))
    
    return {
        'sync_index': sync_index,
        'mean_phase_diff': np.mean(phase_diff),
        'std_phase_diff': np.std(phase_diff)
    }

# Periodic analysis module
def periodogram_analysis(ts, fs=1.0):
    """
    Perform periodogram analysis
    
    Args:
        ts: Time series data
        fs: Sampling frequency
    
    Returns:
        Dictionary containing periodogram analysis results
    """
    freqs, psd = periodogram(ts, fs=fs)
    
    # Identify main periods
    peak_idx = np.argsort(psd)[-3:][::-1]  # Top three peaks
    main_periods = 1 / freqs[peak_idx]
    main_powers = psd[peak_idx]
    
    return {
        'frequencies': freqs,
        'power': psd,
        'main_periods': main_periods,
        'main_powers': main_powers
    }

def spectral_analysis(ts, fs=1.0, nperseg=None):
    """
    Perform spectral analysis (improved version)
    """
    ts = np.asarray(ts)
    if nperseg is None:
        nperseg = min(256, len(ts))
    
    if fs <= 0:
        raise ValueError("Sampling frequency must be positive")
    if nperseg > len(ts):
        raise ValueError("nperseg must not be greater than length of time series")
    
    freqs, psd = welch(ts, fs=fs, nperseg=nperseg)
    
    # Handle zero frequency and Nyquist frequency
    mask = (freqs > 0) & (freqs < fs/2)
    freqs = freqs[mask]
    psd = psd[mask]
    
    if len(psd) == 0:
        return {
            'frequencies': np.array([]),
            'psd': np.array([]),
            'spectral_moment1': 0,
            'spectral_moment2': 0,
            'spectral_bandwidth': 0
        }
    
    total_power = np.sum(psd)
    if total_power > 0:
        spectral_moment1 = np.sum(freqs * psd) / total_power
        spectral_moment2 = np.sum(freqs**2 * psd) / total_power
    else:
        spectral_moment1 = spectral_moment2 = 0
    
    return {
        'frequencies': freqs,
        'psd': psd,
        'spectral_moment1': spectral_moment1,
        'spectral_moment2': spectral_moment2,
        'spectral_bandwidth': np.sqrt(max(0, spectral_moment2 - spectral_moment1**2))
    }

# Nonlinear analysis module
def nonlinear_correlation(x, y, bins=10):
    """
    Calculate nonlinear correlation
    
    Args:
        x: First time series
        y: Second time series
        bins: Number of bins
    
    Returns:
        Dictionary containing nonlinear correlation metrics
    """
    from scipy.stats import spearmanr, kendalltau
    from sklearn.metrics import mutual_info_score
    
    # Spearman correlation coefficient
    spearman_corr, spearman_p = spearman_correlation(x, y)
    
    # Kendall's tau
    kendall_corr, kendall_p = kendall_correlation(x, y)
    
    # Mutual information
    mi = mutual_information(x, y, bins)
    
    return {
        'spearman_correlation': spearman_corr,
        'spearman_pvalue': spearman_p,
        'kendall_correlation': kendall_corr,
        'kendall_pvalue': kendall_p,
        'mutual_information': mi
    }

def phase_space_reconstruction(ts, dim=3, tau=1):
    ts = np.asarray(ts)
    n = len(ts) - (dim - 1) * tau
    
    if n <= 0:
        raise ValueError("Time series too short for given dim and tau")
    
    phase_space = np.zeros((n, dim))
    for i in range(dim):
        phase_space[:, i] = ts[i*tau:i*tau + n]
    
    return phase_space

def lyapunov_exponent(ts, dim=3, tau=1, k=5):
    """
    Calculate maximum Lyapunov exponent
    
    Args:
        ts: Time series data
        dim: Embedding dimension
        tau: Time delay
        k: Number of nearest neighbors
    
    Returns:
        float: Estimated maximum Lyapunov exponent
    """
    # Phase space reconstruction
    phase_space = phase_space_reconstruction(ts, dim, tau)
    
    # Use custom nearest neighbor search function
    distances, indices = find_nearest_neighbors(phase_space[:-1], k)
    
    # Calculate trajectory divergence
    divergence = np.zeros(k)
    for i in range(1, k+1):
        # Use the i-th column of indices (skip the first nearest neighbor, as it's the point itself)
        neighbor_indices = indices[:, i]
        # Calculate trajectory divergence
        divergence[i-1] = np.mean(np.log(np.abs(
            phase_space[1:] - phase_space[neighbor_indices[:-1]]
        )))
    
    # Use custom linear regression function to estimate Lyapunov exponent
    time_points = np.arange(k).reshape(-1, 1)
    slope = linear_regression(time_points.flatten(), divergence)
    
    return slope

def recurrence_quantification(ts, dim=3, tau=1, epsilon=None):
    """
    Perform recurrence quantification analysis (RQA)
    
    Args:
        ts: Time series data
        dim: Embedding dimension
        tau: Time delay
        epsilon: Threshold distance
    
    Returns:
        Dictionary containing RQA metrics
    """
    # Phase space reconstruction
    phase_space = phase_space_reconstruction(ts, dim, tau)
    
    # If epsilon is not specified, use 10% of the phase space diameter
    if epsilon is None:
        epsilon = 0.1 * np.max(np.ptp(phase_space, axis=0))
    
    # Calculate recurrence matrix
    n = len(phase_space)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i, j] = np.linalg.norm(phase_space[i] - phase_space[j])
    
    rec_matrix = dist_matrix < epsilon
    
    # Calculate RQA metrics
    # Recurrence rate
    rec_rate = np.sum(rec_matrix) / (n * n)
    
    # Determinism
    diag_lengths = calculate_diagonal_lengths(rec_matrix)
    
    return {
        'recurrence_rate': rec_rate,
        'determinism': np.sum([l for l in diag_lengths if l >= 2]) / (np.sum(diag_lengths) + 1e-10),
        'average_diagonal_length': np.mean(diag_lengths) if diag_lengths else 0,
        'max_diagonal_length': max(diag_lengths) if diag_lengths else 0
    }

def calculate_diagonal_lengths(rec_matrix):
    """
    Calculate diagonal lengths in recurrence plot (optimized version)
    """
    n = len(rec_matrix)
    diag_lengths = []
    
    def process_diagonal(start_i, start_j):
        i, j = start_i, start_j
        current_length = 0
        while i < n and j < n:
            if rec_matrix[i, j]:
                current_length += 1
            elif current_length > 0:
                diag_lengths.append(current_length)
                current_length = 0
            i += 1
            j += 1
        if current_length > 0:
            diag_lengths.append(current_length)
    
    # Process main diagonal and above (including main diagonal)
    for k in range(n):
        process_diagonal(0, k)
    
    # Process main diagonal and below
    for k in range(1, n):
        process_diagonal(k, 0)
    
    return np.array(diag_lengths)

def spearman_correlation(x, y):
    """
    Calculate Spearman correlation coefficient and p-value
    """
    n = len(x)
    # Calculate ranks
    rank_x = np.argsort(np.argsort(x))
    rank_y = np.argsort(np.argsort(y))
    
    # Calculate correlation coefficient
    mean_x = np.mean(rank_x)
    mean_y = np.mean(rank_y)
    cov = np.sum((rank_x - mean_x) * (rank_y - mean_y))
    std_x = np.sqrt(np.sum((rank_x - mean_x)**2))
    std_y = np.sqrt(np.sum((rank_y - mean_y)**2))
    
    rho = cov / (std_x * std_y)
    
    # Calculate p-value
    t_stat = rho * np.sqrt((n-2)/(1-rho**2))
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n-2))
    
    return rho, p_value

def kendall_correlation(x, y):
    n = len(x)
    pairs = np.array(list(zip(x, y)))
    sorted_pairs = pairs[np.argsort(pairs[:, 0])]
    y_sorted = sorted_pairs[:, 1]
    
    # Use vectorized operations to calculate concordant and discordant pairs
    concordant = discordant = 0
    for i in range(n-1):
        concordant += np.sum(y_sorted[i+1:] > y_sorted[i])
        discordant += np.sum(y_sorted[i+1:] < y_sorted[i])
    
    tau = (concordant - discordant) / (n * (n-1) / 2)
    
    # Calculate p-value
    s = concordant - discordant
    var_s = n * (n - 1) * (2 * n + 5) / 18
    z = s / np.sqrt(var_s)
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    return tau, p_value

def find_nearest_neighbors(X, k):
    X = np.asarray(X)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    
    n_samples = len(X)
    if k >= n_samples:
        raise ValueError("k must be smaller than number of samples")
    
    # Use broadcasting to calculate Euclidean distance matrix
    distances = np.sqrt(np.sum((X[:, np.newaxis, :] - X[np.newaxis, :, :]) ** 2, axis=2))
    
    np.fill_diagonal(distances, np.inf)
    indices = np.argpartition(distances, k, axis=1)[:, :k]
    neighbor_distances = np.take_along_axis(distances, indices, axis=1)
    
    return neighbor_distances, indices

def linear_regression(X, y):
    """
    Simple linear regression implementation (improved version)
    """
    X = np.asarray(X)
    y = np.asarray(y)
    
    if X.ndim != 1 or y.ndim != 1:
        raise ValueError("Input arrays must be one-dimensional")
    if len(X) != len(y):
        raise ValueError("Input arrays must have the same length")
    
    # Add bias term
    X_b = np.c_[np.ones(len(X)), X]
    
    try:
        # Solve using normal equations
        theta = np.linalg.solve(X_b.T @ X_b, X_b.T @ y)
        return theta[1]  # Return slope
    except np.linalg.LinAlgError:
        # Handle singular matrix case
        return np.nan




