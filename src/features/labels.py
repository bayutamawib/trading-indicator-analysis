"""Label creation for price movement prediction"""

import pandas as pd


class LabelCreator:
    """Creates binary labels for price movement prediction"""
    
    def __init__(self, threshold: float = 0.005):
        """Initialize label creator
        
        Args:
            threshold: Price change threshold for "up" label (default: 0.005 = 0.5%)
        """
        self.threshold = threshold
    
    def create_labels(self, df: pd.DataFrame) -> pd.Series:
        """Create binary labels based on next day price movement
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            Series with binary labels (1 for "up", 0 for "down")
        """
        # Calculate next day's close price
        next_close = df["Close"].shift(-1)
        
        # Create labels: 1 if next close > current close * (1 + threshold), else 0
        labels = (next_close > df["Close"] * (1 + self.threshold)).astype(int)
        
        # Remove last row (no next day data)
        labels = labels[:-1]
        
        return labels
    
    def create_labels_with_names(self, df: pd.DataFrame) -> pd.Series:
        """Create labels with string names ("up"/"down")
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            Series with string labels ("up" or "down")
        """
        numeric_labels = self.create_labels(df)
        return numeric_labels.map({1: "up", 0: "down"})
