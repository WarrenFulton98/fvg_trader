import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

@pytest.fixture
def sample_price_data():
    """Create sample price data for testing"""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='5min')
    data = {
        'Open': np.random.normal(100, 1, 100),
        'High': np.random.normal(101, 1, 100),
        'Low': np.random.normal(99, 1, 100),
        'Close': np.random.normal(100, 1, 100),
        'Volume': np.random.normal(1000000, 100000, 100)
    }
    df = pd.DataFrame(data, index=dates)
    # Ensure High is highest and Low is lowest
    df['High'] = df[['Open', 'High', 'Close']].max(axis=1) + 0.1
    df['Low'] = df[['Open', 'Low', 'Close']].min(axis=1) - 0.1
    return df

@pytest.fixture
def sample_fvg_data():
    """Create sample data with known FVGs"""
    dates = pd.date_range(start='2024-01-01', periods=5, freq='5min')
    data = {
        'Open':  [100, 100, 100, 104, 104],
        'High':  [101, 101, 101, 105, 105],
        'Low':   [99,  99,  99,  103, 103],
        'Close': [100, 100, 100, 104, 104],
        'Volume': [1000000] * 5
    }
    return pd.DataFrame(data, index=dates)
