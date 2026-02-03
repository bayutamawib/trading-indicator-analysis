"""Base class for technical indicator calculators"""

from abc import ABC, abstractmethod
import pandas as pd


class IndicatorCalculator(ABC):
    """Abstract base class for technical indicator calculators"""
    
    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate indicator and return DataFrame with indicator column(s)
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with original data plus indicator column(s)
        """
        pass
    
    @staticmethod
    def _handle_nans(df: pd.DataFrame, method: str = "ffill") -> pd.DataFrame:
        """Handle NaN values in DataFrame
        
        Args:
            df: DataFrame with potential NaN values
            method: Method to handle NaNs ('ffill' for forward-fill, 'dropna' for removal)
        
        Returns:
            DataFrame with NaNs handled
        """
        if method == "ffill":
            return df.ffill().bfill()
        elif method == "dropna":
            return df.dropna()
        else:
            raise ValueError(f"Unknown NaN handling method: {method}")
