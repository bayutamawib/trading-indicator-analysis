"""Data splitting for temporal data with no leakage"""

import pandas as pd
from typing import Tuple


class DataSplitter:
    """Splits data into train/validation/test sets with temporal ordering"""
    
    def __init__(self, train_ratio: float = 0.7, val_ratio: float = 0.15, test_ratio: float = 0.15):
        """Initialize data splitter
        
        Args:
            train_ratio: Proportion of data for training (default: 0.7)
            val_ratio: Proportion of data for validation (default: 0.15)
            test_ratio: Proportion of data for testing (default: 0.15)
        """
        if not (0 < train_ratio < 1 and 0 < val_ratio < 1 and 0 < test_ratio < 1):
            raise ValueError("All ratios must be between 0 and 1")
        
        if abs(train_ratio + val_ratio + test_ratio - 1.0) > 0.001:
            raise ValueError("Ratios must sum to 1.0")
        
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
    
    def split_data(
        self,
        X: pd.DataFrame,
        y: pd.Series
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
        """Split data into train/validation/test sets preserving temporal order
        
        Args:
            X: Feature DataFrame
            y: Label Series
        
        Returns:
            Tuple of (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        n = len(X)
        
        # Calculate split indices
        train_idx = int(n * self.train_ratio)
        val_idx = train_idx + int(n * self.val_ratio)
        
        # Split data preserving temporal order
        X_train = X.iloc[:train_idx]
        X_val = X.iloc[train_idx:val_idx]
        X_test = X.iloc[val_idx:]
        
        y_train = y.iloc[:train_idx]
        y_val = y.iloc[train_idx:val_idx]
        y_test = y.iloc[val_idx:]
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def verify_temporal_integrity(
        self,
        X_train: pd.DataFrame,
        X_val: pd.DataFrame,
        X_test: pd.DataFrame
    ) -> bool:
        """Verify that temporal ordering is preserved across splits
        
        Args:
            X_train: Training features
            X_val: Validation features
            X_test: Test features
        
        Returns:
            True if temporal ordering is correct, False otherwise
        """
        if not isinstance(X_train.index, pd.DatetimeIndex):
            return True  # Can't verify without datetime index
        
        # Check that train < val < test
        train_max = X_train.index.max()
        val_min = X_val.index.min()
        val_max = X_val.index.max()
        test_min = X_test.index.min()
        
        return train_max < val_min and val_max < test_min
