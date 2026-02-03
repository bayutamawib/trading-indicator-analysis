"""Visualization of analysis results"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple


class Visualizer:
    """Creates visualizations for analysis results"""
    
    def __init__(self, output_dir: str = "reports/visualizations"):
        """Initialize visualizer
        
        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_style("whitegrid")
    
    def plot_feature_importance(
        self,
        feature_importance: Dict[str, float],
        top_n: int = 15,
        save_path: str = None
    ) -> str:
        """Plot feature importance
        
        Args:
            feature_importance: Dictionary mapping feature to importance
            top_n: Number of top features to display
            save_path: Path to save figure
        
        Returns:
            Path to saved figure
        """
        # Sort and get top N
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        top_features = sorted_features[:top_n]
        
        names = [f[0] for f in top_features]
        values = [f[1] for f in top_features]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(names, values, color="steelblue")
        ax.set_xlabel("Importance Score")
        ax.set_title(f"Top {top_n} Feature Importance")
        ax.invert_yaxis()
        
        plt.tight_layout()
        
        # Save
        if save_path is None:
            save_path = self.output_dir / "feature_importance.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()
        
        return str(save_path)
    
    def plot_confusion_matrix(
        self,
        cm: np.ndarray,
        labels: List[str] = None,
        save_path: str = None
    ) -> str:
        """Plot confusion matrix
        
        Args:
            cm: Confusion matrix
            labels: Class labels
            save_path: Path to save figure
        
        Returns:
            Path to saved figure
        """
        if labels is None:
            labels = ["Down", "Up"]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels, ax=ax)
        ax.set_ylabel("True Label")
        ax.set_xlabel("Predicted Label")
        ax.set_title("Confusion Matrix")
        
        plt.tight_layout()
        
        # Save
        if save_path is None:
            save_path = self.output_dir / "confusion_matrix.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()
        
        return str(save_path)
    
    def plot_roc_curve(
        self,
        fpr: np.ndarray,
        tpr: np.ndarray,
        auc_score: float,
        save_path: str = None
    ) -> str:
        """Plot ROC curve
        
        Args:
            fpr: False positive rates
            tpr: True positive rates
            auc_score: ROC-AUC score
            save_path: Path to save figure
        
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {auc_score:.3f})")
        ax.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--", label="Random Classifier")
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curve")
        ax.legend(loc="lower right")
        
        plt.tight_layout()
        
        # Save
        if save_path is None:
            save_path = self.output_dir / "roc_curve.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()
        
        return str(save_path)
    
    def plot_indicator_correlation(
        self,
        correlations: Dict[str, float],
        save_path: str = None
    ) -> str:
        """Plot indicator correlations
        
        Args:
            correlations: Dictionary mapping indicator to correlation
            save_path: Path to save figure
        
        Returns:
            Path to saved figure
        """
        # Sort correlations
        sorted_corr = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
        names = [c[0] for c in sorted_corr]
        values = [c[1] for c in sorted_corr]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = ["green" if v > 0 else "red" for v in values]
        ax.barh(names, values, color=colors, alpha=0.7)
        ax.set_xlabel("Correlation with Price Movement")
        ax.set_title("Indicator Correlation Analysis")
        ax.invert_yaxis()
        
        plt.tight_layout()
        
        # Save
        if save_path is None:
            save_path = self.output_dir / "indicator_correlation.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()
        
        return str(save_path)
