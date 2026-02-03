"""MACD (Moving Average Convergence Divergence) indicator calculation"""

import pandas as pd
from .base import IndicatorCalculator


class MACDCalculator(IndicatorCalculator):
    """Calculates MACD indicator"""
    
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        """Initialize MACD calculator
        
        Args:
            fast_period: Fast EMA period (default: 12)
            slow_period: Slow EMA period (default: 26)
            signal_period: Signal line EMA period (default: 9)
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate MACD indicator
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with MACD columns added
        """
        df = df.copy()
        
        # Calculate exponential moving averages
        ema_fast = df["Close"].ewm(span=self.fast_period).mean()
        ema_slow = df["Close"].ewm(span=self.slow_period).mean()
        
        # Calculate MACD line
        df["MACD"] = ema_fast - ema_slow
        
        # Calculate signal line
        df["MACD_Signal"] = df["MACD"].ewm(span=self.signal_period).mean()
        
        # Calculate histogram
        df["MACD_Histogram"] = df["MACD"] - df["MACD_Signal"]
        
        # Handle NaNs
        df = self._handle_nans(df, method="ffill")
        
        return df
