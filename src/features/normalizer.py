"""Feature normalization using StandardScaler"""

import pandas as pd
from sklearn.preprocessing import StandardScaler


class FeatureNormalizer:
    """Normalizes indicator features to zero mean and unit variance"""
    
    def __init__(self):
        """Initialize feature normalizer"""
        self.scaler = StandardScaler()
        self.feature_names = None
    
    def fit(self, df: pd.DataFrame, feature_columns: list) -> None:
        """Fit scaler on training data
        
        Args:
            df: DataFrame with features
            feature_columns: List of feature column names to normalize
        """
        self.feature_names = feature_columns
        self.scaler.fit(df[feature_columns])
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform features using fitted scaler
        
        Args:
            df: DataFrame with features
        
        Returns:
            DataFrame with normalized features
        """
        if self.feature_names is None:
            raise ValueError("Normalizer not fitted. Call fit() first.")
        
        df_normalized = df.copy()
        df_normalized[self.feature_names] = self.scaler.transform(df[self.feature_names])
        
        return df_normalized
    
    def fit_transform(self, df: pd.DataFrame, feature_columns: list) -> pd.DataFrame:
        """Fit scaler and transform features
        
        Args:
            df: DataFrame with features
            feature_columns: List of feature column names to normalize
        
        Returns:
            DataFrame with normalized features
        """
        self.fit(df, feature_columns)
        return self.transform(df)
    
    def inverse_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Inverse transform normalized features back to original scale
        
        Args:
            df: DataFrame with normalized features
        
        Returns:
            DataFrame with original scale features
        """
        if self.feature_names is None:
            raise ValueError("Normalizer not fitted. Call fit() first.")
        
        df_original = df.copy()
        df_original[self.feature_names] = self.scaler.inverse_transform(df[self.feature_names])
        
        return df_original
