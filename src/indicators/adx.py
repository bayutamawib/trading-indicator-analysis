"""ADX (Average Directional Index) indicator calculation"""

import pandas as pd
from .base import IndicatorCalculator


class ADXCalculator(IndicatorCalculator):
    """Calculates ADX indicator"""
    
    def __init__(self, period: int = 14):
        """Initialize ADX calculator
        
        Args:
            period: Period for ADX calculation (default: 14)
        """
        self.period = period
    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate ADX indicator
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with ADX column added
        """
        df = df.copy()
        
        # Calculate directional movements
        high_diff = df["High"].diff()
        low_diff = -df["Low"].diff()
        
        # Determine positive and negative directional movements
        plus_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
        minus_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)
        
        # Calculate true range
        high_low = df["High"] - df["Low"]
        high_close = abs(df["High"] - df["Close"].shift())
        low_close = abs(df["Low"] - df["Close"].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        
        # Calculate directional indicators
        plus_di = 100 * (plus_dm.rolling(window=self.period).sum() / true_range.rolling(window=self.period).sum())
        minus_di = 100 * (minus_dm.rolling(window=self.period).sum() / true_range.rolling(window=self.period).sum())
        
        # Calculate DX
        di_sum = plus_di + minus_di
        dx = 100 * abs(plus_di - minus_di) / di_sum
        
        # Calculate ADX
        df["ADX"] = dx.rolling(window=self.period).mean()
        
        # Handle NaNs
        df = self._handle_nans(df, method="ffill")
        
        return df
