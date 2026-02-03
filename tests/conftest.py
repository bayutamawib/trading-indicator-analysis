"""Pytest configuration and fixtures"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


@pytest.fixture
def sample_ohlcv_data():
    """Generate sample OHLCV data for testing"""
    dates = pd.date_range(start="2023-01-01", periods=500, freq="D")
    np.random.seed(42)
    
    close = 100 + np.cumsum(np.random.randn(500) * 2)
    high = close + np.abs(np.random.randn(500))
    low = close - np.abs(np.random.randn(500))
    open_price = close + np.random.randn(500) * 0.5
    volume = np.random.randint(1000000, 10000000, 500)
    
    df = pd.DataFrame({
        "Date": dates,
        "Open": open_price,
        "High": high,
        "Low": low,
        "Close": close,
        "Volume": volume
    })
    
    return df.set_index("Date")


@pytest.fixture
def sample_indicators_data(sample_ohlcv_data):
    """Generate sample data with indicators"""
    df = sample_ohlcv_data.copy()
    
    # Add dummy indicators
    df["ATR"] = np.random.rand(len(df)) * 2 + 1
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["SMA_50"] = df["Close"].rolling(50).mean()
    df["RSI"] = np.random.rand(len(df)) * 100
    
    return df
