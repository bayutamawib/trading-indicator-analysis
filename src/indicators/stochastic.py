"""Stochastic Oscillator indicator calculation"""

import pandas as pd
from .base import IndicatorCalculator


class StochasticCalculator(IndicatorCalculator):
    """Calculates Stochastic Oscillator indicator"""
    
    def __init__(self, period: int = 14, smoothing: int = 3):
        """Initialize Stochastic calculator
        
        Args:
            period: Period for Stochastic calculation (default: 14)
            smoothing: Smoothing period for %D (default: 3)
        """
        self.period = period
        self.smoothing = smoothing
    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Stochastic Oscillator
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with Stochastic columns added
        """
        df = df.copy()
        
        # Calculate lowest low and highest high
        lowest_low = df["Low"].rolling(window=self.period).min()
        highest_high = df["High"].rolling(window=self.period).max()
        
        # Calculate %K
        df["Stoch_K"] = 100 * (df["Close"] - lowest_low) / (highest_high - lowest_low)
        
        # Calculate %D (smoothed %K)
        df["Stoch_D"] = df["Stoch_K"].rolling(window=self.smoothing).mean()
        
        # Handle NaNs
        df = self._handle_nans(df, method="ffill")
        
        return df
