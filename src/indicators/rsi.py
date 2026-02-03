"""Relative Strength Index (RSI) indicator calculation"""

import pandas as pd
from .base import IndicatorCalculator


class RSICalculator(IndicatorCalculator):
    """Calculates Relative Strength Index (RSI) indicator"""
    
    def __init__(self, period: int = 14):
        """Initialize RSI calculator
        
        Args:
            period: Period for RSI calculation (default: 14)
        """
        self.period = period
    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate RSI indicator
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with RSI column added
        """
        df = df.copy()
        
        # Calculate price changes
        delta = df["Close"].diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gains = gains.rolling(window=self.period).mean()
        avg_losses = losses.rolling(window=self.period).mean()
        
        # Calculate RS and RSI
        rs = avg_gains / avg_losses
        df["RSI"] = 100 - (100 / (1 + rs))
        
        # Handle NaNs
        df = self._handle_nans(df, method="ffill")
        
        return df
