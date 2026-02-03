"""Average True Range (ATR) indicator calculation"""

import pandas as pd
from .base import IndicatorCalculator


class ATRCalculator(IndicatorCalculator):
    """Calculates Average True Range (ATR) indicator"""
    
    def __init__(self, period: int = 14):
        """Initialize ATR calculator
        
        Args:
            period: Period for ATR calculation (default: 14)
        """
        self.period = period
    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate ATR indicator
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with ATR column added
        """
        df = df.copy()
        
        # Calculate True Range
        high_low = df["High"] - df["Low"]
        high_close = abs(df["High"] - df["Close"].shift())
        low_close = abs(df["Low"] - df["Close"].shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        
        # Calculate ATR as rolling average of True Range
        df["ATR"] = true_range.rolling(window=self.period).mean()
        
        # Handle NaNs
        df = self._handle_nans(df, method="ffill")
        
        return df
