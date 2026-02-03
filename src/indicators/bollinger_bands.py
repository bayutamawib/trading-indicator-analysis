"""Bollinger Bands indicator calculation"""

import pandas as pd
from .base import IndicatorCalculator


class BollingerBandsCalculator(IndicatorCalculator):
    """Calculates Bollinger Bands indicator"""
    
    def __init__(self, period: int = 20, std_dev: float = 2.0):
        """Initialize Bollinger Bands calculator
        
        Args:
            period: Period for moving average (default: 20)
            std_dev: Number of standard deviations (default: 2.0)
        """
        self.period = period
        self.std_dev = std_dev
    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Bollinger Bands
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with Bollinger Bands columns added
        """
        df = df.copy()
        
        # Calculate middle band (SMA)
        df["BB_Middle"] = df["Close"].rolling(window=self.period).mean()
        
        # Calculate standard deviation
        std = df["Close"].rolling(window=self.period).std()
        
        # Calculate upper and lower bands
        df["BB_Upper"] = df["BB_Middle"] + (std * self.std_dev)
        df["BB_Lower"] = df["BB_Middle"] - (std * self.std_dev)
        
        # Handle NaNs
        df = self._handle_nans(df, method="ffill")
        
        return df
