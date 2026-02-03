"""Model evaluation orchestrator"""

import pandas as pd
from typing import Dict, Any

from .metrics import MetricsCalculator
from .analyzer import IndicatorAnalyzer
from .reporter import ReportGenerator
from .visualizer import Visualizer


class Evaluator:
    """Orchestrates model evaluation pipeline"""
    
    def __init__(self, report_dir: str = "reports"):
        """Initialize evaluator
        
        Args:
            report_dir: Directory to save reports and visualizations
        """
        self.metrics_calc = MetricsCalculator()
        self.analyzer = IndicatorAnalyzer()
        self.reporter = ReportGenerator(report_dir)
        self.visualizer = Visualizer(f"{report_dir}/visualizations")
    
    def evaluate_model(
        self,
        model: Any,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        X_full: pd.DataFrame,
        y_full: pd.Series,
        feature_names: list,
        stock_ticker: str = "UNKNOWN"
    ) -> Dict[str, Any]:
        """Evaluate model and generate comprehensive report
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            X_full: Full dataset features (for correlation analysis)
            y_full: Full dataset labels
            feature_names: List of feature names
            stock_ticker: Stock ticker symbol
        
        Returns:
            Dictionary with evaluation results
        """
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Calculate metrics
        metrics = self.metrics_calc.compute_all_metrics(y_test, y_pred, y_pred_proba)
        
        # Get feature importance
        feature_importance = dict(zip(feature_names, model.feature_importances_))
        
        # Compute correlations
        correlations = self.analyzer.compute_indicator_correlation(X_full, y_full, feature_names)
        
        # Generate insights
        insights = self.analyzer.generate_insights(feature_importance, correlations, metrics)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, feature_importance)
        
        # Generate report
        report = self.reporter.generate_report(
            stock_ticker,
            metrics,
            feature_importance,
            correlations,
            insights,
            recommendations
        )
        
        # Save reports to files
        report_paths = self.reporter.save_report(report)
        
        # Create visualizations
        viz_paths = {
            "feature_importance": self.visualizer.plot_feature_importance(feature_importance),
            "confusion_matrix": self.visualizer.plot_confusion_matrix(metrics["confusion_matrix"]),
            "indicator_correlation": self.visualizer.plot_indicator_correlation(correlations),
        }
        
        if "roc_auc" in metrics:
            viz_paths["roc_curve"] = self.visualizer.plot_roc_curve(
                metrics["fpr"],
                metrics["tpr"],
                metrics["roc_auc"]
            )
        
        return {
            "metrics": metrics,
            "feature_importance": feature_importance,
            "correlations": correlations,
            "report": report,
            "report_paths": report_paths,
            "visualizations": viz_paths,
            "text_report": self.reporter.generate_text_report(report),
        }
    
    def _generate_recommendations(
        self,
        metrics: Dict[str, Any],
        feature_importance: Dict[str, float]
    ) -> list:
        """Generate recommendations based on evaluation results
        
        Args:
            metrics: Model metrics
            feature_importance: Feature importance scores
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Accuracy-based recommendations
        accuracy = metrics.get("accuracy", 0)
        if accuracy < 0.55:
            recommendations.append("Model accuracy is below 55%. Consider collecting more data or adjusting features.")
        elif accuracy < 0.60:
            recommendations.append("Model shows moderate performance. Consider feature engineering or hyperparameter tuning.")
        
        # Feature-based recommendations
        top_indicators = self.analyzer.get_top_indicators(feature_importance, top_n=3)
        recommendations.append(f"Focus trading strategy on top indicators: {', '.join(top_indicators)}")
        
        # Precision/Recall recommendations
        precision = metrics.get("precision", 0)
        recall = metrics.get("recall", 0)
        
        if precision > recall:
            recommendations.append("Model has high precision but lower recall. Consider adjusting decision threshold to catch more positive cases.")
        elif recall > precision:
            recommendations.append("Model has high recall but lower precision. Consider adjusting decision threshold to reduce false positives.")
        
        return recommendations
