"""Metrics calculation for model evaluation"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from typing import Dict, Any, Tuple


class MetricsCalculator:
    """Calculates evaluation metrics for model predictions"""
    
    @staticmethod
    def compute_accuracy(y_true: pd.Series, y_pred: pd.Series) -> float:
        """Compute accuracy score
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
        
        Returns:
            Accuracy score
        """
        return accuracy_score(y_true, y_pred)
    
    @staticmethod
    def compute_precision_recall_f1(
        y_true: pd.Series,
        y_pred: pd.Series,
        average: str = "weighted"
    ) -> Dict[str, float]:
        """Compute precision, recall, and F1-score
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            average: Averaging method ('weighted', 'macro', 'micro')
        
        Returns:
            Dictionary with precision, recall, and F1-score
        """
        return {
            "precision": precision_score(y_true, y_pred, average=average, zero_division=0),
            "recall": recall_score(y_true, y_pred, average=average, zero_division=0),
            "f1_score": f1_score(y_true, y_pred, average=average, zero_division=0),
        }
    
    @staticmethod
    def compute_confusion_matrix(y_true: pd.Series, y_pred: pd.Series) -> np.ndarray:
        """Compute confusion matrix
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
        
        Returns:
            Confusion matrix
        """
        return confusion_matrix(y_true, y_pred)
    
    @staticmethod
    def compute_roc_auc(y_true: pd.Series, y_pred_proba: pd.DataFrame) -> Tuple[float, np.ndarray, np.ndarray]:
        """Compute ROC-AUC score and curve
        
        Args:
            y_true: True labels
            y_pred_proba: Prediction probabilities
        
        Returns:
            Tuple of (ROC-AUC score, FPR, TPR)
        """
        # Get probability for positive class
        if isinstance(y_pred_proba, pd.DataFrame):
            y_proba = y_pred_proba.iloc[:, 1].values
        else:
            y_proba = y_pred_proba[:, 1]
        
        auc_score = roc_auc_score(y_true, y_proba)
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        
        return auc_score, fpr, tpr
    
    @staticmethod
    def compute_all_metrics(
        y_true: pd.Series,
        y_pred: pd.Series,
        y_pred_proba: pd.DataFrame = None
    ) -> Dict[str, Any]:
        """Compute all evaluation metrics
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Prediction probabilities (optional)
        
        Returns:
            Dictionary with all metrics
        """
        metrics = {
            "accuracy": MetricsCalculator.compute_accuracy(y_true, y_pred),
        }
        
        # Add precision, recall, F1
        metrics.update(MetricsCalculator.compute_precision_recall_f1(y_true, y_pred))
        
        # Add confusion matrix
        cm = MetricsCalculator.compute_confusion_matrix(y_true, y_pred)
        metrics["confusion_matrix"] = cm.tolist()
        
        # Add ROC-AUC if probabilities provided
        if y_pred_proba is not None:
            auc_score, fpr, tpr = MetricsCalculator.compute_roc_auc(y_true, y_pred_proba)
            metrics["roc_auc"] = auc_score
            metrics["fpr"] = fpr.tolist()
            metrics["tpr"] = tpr.tolist()
        
        return metrics
