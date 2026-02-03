"""Indicator performance analysis"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class IndicatorAnalyzer:
    """Analyzes indicator performance and importance"""
    
    @staticmethod
    def rank_indicators_by_importance(
        feature_importance: Dict[str, float]
    ) -> List[Tuple[str, float]]:
        """Rank indicators by feature importance
        
        Args:
            feature_importance: Dictionary mapping indicator name to importance score
        
        Returns:
            List of (indicator, importance) tuples sorted by importance
        """
        ranked = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        return ranked
    
    @staticmethod
    def compute_indicator_correlation(
        df: pd.DataFrame,
        labels: pd.Series,
        indicator_columns: List[str]
    ) -> Dict[str, float]:
        """Compute correlation between each indicator and price movements
        
        Args:
            df: DataFrame with indicators
            labels: Binary labels (0/1)
            indicator_columns: List of indicator column names
        
        Returns:
            Dictionary mapping indicator to correlation with labels
        """
        correlations = {}
        
        for col in indicator_columns:
            if col in df.columns:
                # Calculate correlation with labels
                corr = df[col].corr(labels)
                correlations[col] = abs(corr) if not np.isnan(corr) else 0.0
        
        return dict(sorted(correlations.items(), key=lambda x: x[1], reverse=True))
    
    @staticmethod
    def identify_top_combinations(
        feature_importance: Dict[str, float],
        top_n: int = 3
    ) -> List[List[str]]:
        """Identify top indicator combinations
        
        Args:
            feature_importance: Dictionary mapping indicator to importance
            top_n: Number of top indicators to consider
        
        Returns:
            List of top indicator combinations
        """
        ranked = IndicatorAnalyzer.rank_indicators_by_importance(feature_importance)
        top_indicators = [ind for ind, _ in ranked[:top_n]]
        
        # Generate combinations
        combinations = [
            top_indicators[:1],
            top_indicators[:2],
            top_indicators[:3],
        ]
        
        return combinations
    
    @staticmethod
    def get_top_indicators(
        feature_importance: Dict[str, float],
        top_n: int = 3
    ) -> List[str]:
        """Get top N most important indicators
        
        Args:
            feature_importance: Dictionary mapping indicator to importance
            top_n: Number of top indicators to return
        
        Returns:
            List of top indicator names
        """
        ranked = IndicatorAnalyzer.rank_indicators_by_importance(feature_importance)
        return [ind for ind, _ in ranked[:top_n]]
    
    @staticmethod
    def generate_insights(
        feature_importance: Dict[str, float],
        correlations: Dict[str, float],
        metrics: Dict[str, float]
    ) -> List[str]:
        """Generate actionable insights from analysis
        
        Args:
            feature_importance: Feature importance scores
            correlations: Indicator correlations with labels
            metrics: Model performance metrics
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Top indicators insight
        top_indicators = IndicatorAnalyzer.get_top_indicators(feature_importance, top_n=3)
        insights.append(f"Top 3 most predictive indicators: {', '.join(top_indicators)}")
        
        # Model performance insight
        accuracy = metrics.get("accuracy", 0)
        if accuracy > 0.6:
            insights.append(f"Model shows good predictive power with {accuracy:.1%} accuracy")
        elif accuracy > 0.55:
            insights.append(f"Model shows moderate predictive power with {accuracy:.1%} accuracy")
        else:
            insights.append(f"Model shows weak predictive power with {accuracy:.1%} accuracy")
        
        # Correlation insight
        high_corr_indicators = [ind for ind, corr in correlations.items() if corr > 0.3]
        if high_corr_indicators:
            insights.append(f"Indicators with strong correlation to price movements: {', '.join(high_corr_indicators)}")
        
        return insights
