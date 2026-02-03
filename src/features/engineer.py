"""Feature engineering orchestrator"""

import pandas as pd
from typing import Tuple, Dict, Any

from .normalizer import FeatureNormalizer
from .labels import LabelCreator
from .splitter import DataSplitter
from .balancer import ClassBalancer


class FeatureEngineer:
    """Orchestrates feature engineering pipeline"""
    
    def __init__(self, indicator_columns: list = None):
        """Initialize feature engineer
        
        Args:
            indicator_columns: List of indicator column names to use as features
        """
        self.indicator_columns = indicator_columns or []
        self.normalizer = FeatureNormalizer()
        self.label_creator = LabelCreator(threshold=0.005)
        self.splitter = DataSplitter(train_ratio=0.7, val_ratio=0.15, test_ratio=0.15)
        self.balancer = ClassBalancer()
        self.metadata = {}
    
    def prepare_features(
        self,
        df: pd.DataFrame,
        apply_balancing: bool = True
    ) -> Dict[str, Any]:
        """Prepare features for model training
        
        Args:
            df: DataFrame with OHLCV data and indicators
            apply_balancing: Whether to apply class balancing
        
        Returns:
            Dictionary with train/val/test sets and metadata
        """
        # Create labels
        labels = self.label_creator.create_labels(df)
        
        # Remove last row from features (no label for last row)
        features = df[:-1].copy()
        
        # Select indicator columns
        if not self.indicator_columns:
            raise ValueError("No indicator columns specified")
        
        X = features[self.indicator_columns]
        y = labels
        
        # Normalize features
        X_normalized = self.normalizer.fit_transform(X, self.indicator_columns)
        
        # Detect class imbalance
        imbalance_info = self.balancer.detect_imbalance(y)
        
        # Apply balancing if needed
        if apply_balancing and imbalance_info["is_imbalanced"]:
            X_normalized, y = self.balancer.balance_data_smote(X_normalized, y)
        
        # Compute class weights
        class_weights = self.balancer.compute_class_weights(y)
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test = self.splitter.split_data(X_normalized, y)
        
        # Store metadata
        self.metadata = {
            "n_features": len(self.indicator_columns),
            "feature_names": self.indicator_columns,
            "n_samples": len(X),
            "n_train": len(X_train),
            "n_val": len(X_val),
            "n_test": len(X_test),
            "class_distribution": imbalance_info["class_distribution"],
            "is_imbalanced": imbalance_info["is_imbalanced"],
            "class_weights": class_weights,
        }
        
        return {
            "X_train": X_train,
            "X_val": X_val,
            "X_test": X_test,
            "y_train": y_train,
            "y_val": y_val,
            "y_test": y_test,
            "metadata": self.metadata,
            "normalizer": self.normalizer,
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get feature engineering metadata
        
        Returns:
            Dictionary with metadata
        """
        return self.metadata
