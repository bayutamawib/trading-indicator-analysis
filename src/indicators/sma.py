"""Simple Moving Average (SMA) indicator calculation"""

import pandas as pd
from .base import IndicatorCalculator


class SMACalculator(IndicatorCalculator):
    """Calculates Simple Moving Average (SMA) indicators"""
    
    def __init__(self, periods: list = None):
        """Initialize SMA calculator
        
        Args:
            periods: List of periods for SMA calculation (default: [20, 50])
        """
        self.periods = periods or [20, 50]
    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate SMA indicators
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with SMA columns added
        """
        df = df.copy()
        
        for period in self.periods:
            col_name = f"SMA_{period}"
            df[col_name] = df["Close"].rolling(window=period).mean()
        
        # Handle NaNs
        df = self._handle_nans(df, method="ffill")
        
        return df
