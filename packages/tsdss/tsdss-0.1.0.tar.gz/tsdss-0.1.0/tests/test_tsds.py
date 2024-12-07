import numpy as np
import pandas as pd
import pytest
from tsdss import (
    ts_statistics,
    normalize_ts,
    calculate_entropy,
    iaaft,
    ipft,
    aiaaft,
    block_bootstrap,
    stationary_bootstrap
)

@pytest.fixture
def sample_data():
    np.random.seed(42)
    return np.random.normal(0, 1, 1000)

@pytest.fixture
def mv_sample_data():
    np.random.seed(42)
    return np.random.normal(0, 1, (1000, 3))

def test_basic_statistics(sample_data):
    stats = ts_statistics(sample_data)
    assert isinstance(stats, pd.DataFrame)
    assert 'Mean' in stats.columns
    assert 'Std Dev' in stats.columns
    assert 'Skewness' in stats.columns
    assert 'Kurtosis' in stats.columns
    assert stats.shape[0] == 1  # One row for single series

def test_surrogate_methods(sample_data):
    # Test IAAFT
    surrogate = iaaft(sample_data, n_iterations=100, num_surrogates=1)[0]
    assert len(surrogate) == len(sample_data)
    assert np.allclose(np.mean(surrogate), np.mean(sample_data), rtol=1e-1)
    
    # Test IPFT
    surrogate = ipft(sample_data, n_iterations=100, num_surrogates=1)[0]
    assert len(surrogate) == len(sample_data)
    
    # Test AIAAFT
    surrogate = aiaaft(sample_data, n_iterations=100, num_surrogates=1)[0]
    assert len(surrogate) == len(sample_data)

def test_bootstrap_methods(sample_data):
    # Test block bootstrap
    samples = block_bootstrap(sample_data, block_length=50, num_bootstrap=10)
    assert len(samples) == 10
    assert len(samples[0]) == len(sample_data)
    
    # Test stationary bootstrap
    samples = stationary_bootstrap(sample_data, mean_block_length=50, num_bootstrap=10)
    assert len(samples) == 10
    assert len(samples[0]) == len(sample_data)

def test_normalize_ts(sample_data):
    normalized = normalize_ts(sample_data, method='zscore')
    assert np.abs(np.mean(normalized)) < 1e-10
    assert np.abs(np.std(normalized) - 1.0) < 1e-10

def test_entropy(sample_data):
    entropy = calculate_entropy(sample_data)
    assert isinstance(entropy, float)
    assert entropy > 0 or np.isinf(entropy)