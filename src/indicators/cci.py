"""CCI (Commodity Channel Index) indicator calculation"""

import pandas as pd
from .base import IndicatorCalculator


class CCICalculator(IndicatorCalculator):
    """Calculates CCI indicator"""
    
    def __init__(self, period: int = 20):
        """Initialize CCI calculator
        
        Args:
            period: Period for CCI calculation (default: 20)
        """
        self.period = period
    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate CCI indicator
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with CCI column added
        """
        df = df.copy()
        
        # Calculate typical price
        typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
        
        # Calculate SMA of typical price
        sma_tp = typical_price.rolling(window=self.period).mean()
        
        # Calculate mean deviation
        mean_dev = typical_price.rolling(window=self.period).apply(
            lambda x: abs(x - x.mean()).mean()
        )
        
        # Calculate CCI
        df["CCI"] = (typical_price - sma_tp) / (0.015 * mean_dev)
        
        # Handle NaNs
        df = self._handle_nans(df, method="ffill")
        
        return df
