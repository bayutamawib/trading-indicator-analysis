"""Class imbalance detection and handling"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional


class ClassBalancer:
    """Detects and handles class imbalance in labels"""
    
    def __init__(self, imbalance_threshold: float = 0.3):
        """Initialize class balancer
        
        Args:
            imbalance_threshold: Threshold for detecting imbalance (default: 0.3)
        """
        self.imbalance_threshold = imbalance_threshold
        self.class_weights = None
    
    def detect_imbalance(self, y: pd.Series) -> dict:
        """Detect class imbalance in labels
        
        Args:
            y: Label series
        
        Returns:
            Dictionary with imbalance information
        """
        value_counts = y.value_counts(normalize=True)
        
        # Calculate imbalance ratio
        if len(value_counts) == 2:
            ratio = value_counts.iloc[0] / value_counts.iloc[1]
            imbalance_ratio = max(ratio, 1/ratio)
        else:
            imbalance_ratio = 1.0
        
        is_imbalanced = imbalance_ratio > (1 + self.imbalance_threshold)
        
        return {
            "is_imbalanced": is_imbalanced,
            "imbalance_ratio": imbalance_ratio,
            "class_distribution": value_counts.to_dict(),
            "threshold": 1 + self.imbalance_threshold
        }
    
    def compute_class_weights(self, y: pd.Series) -> dict:
        """Compute class weights for imbalanced data
        
        Args:
            y: Label series
        
        Returns:
            Dictionary mapping class to weight
        """
        value_counts = y.value_counts()
        total = len(y)
        
        weights = {}
        for class_label, count in value_counts.items():
            weights[class_label] = total / (len(value_counts) * count)
        
        self.class_weights = weights
        return weights
    
    def balance_data_smote(
        self,
        X: pd.DataFrame,
        y: pd.Series
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Balance data using SMOTE (Synthetic Minority Over-sampling Technique)
        
        Args:
            X: Feature DataFrame
            y: Label series
        
        Returns:
            Tuple of balanced (X, y)
        """
        try:
            from imblearn.over_sampling import SMOTE
            
            smote = SMOTE(random_state=42)
            X_balanced, y_balanced = smote.fit_resample(X, y)
            
            return pd.DataFrame(X_balanced, columns=X.columns), pd.Series(y_balanced)
        
        except ImportError:
            # If imblearn not available, return original data
            return X, y
    
    def get_class_weights_dict(self) -> Optional[dict]:
        """Get computed class weights
        
        Returns:
            Dictionary of class weights or None if not computed
        """
        return self.class_weights
