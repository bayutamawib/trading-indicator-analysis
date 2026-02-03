"""Report generation for analysis results"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


class ReportGenerator:
    """Generates analysis reports"""
    
    def __init__(self, report_dir: str = "reports"):
        """Initialize report generator
        
        Args:
            report_dir: Directory to save reports
        """
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(
        self,
        stock_ticker: str,
        metrics: Dict[str, Any],
        feature_importance: Dict[str, float],
        correlations: Dict[str, float],
        insights: List[str],
        recommendations: List[str] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive analysis report
        
        Args:
            stock_ticker: Stock ticker symbol
            metrics: Model performance metrics
            feature_importance: Feature importance scores
            correlations: Indicator correlations
            insights: List of insights
            recommendations: List of recommendations
        
        Returns:
            Report dictionary
        """
        if recommendations is None:
            recommendations = []
        
        # Get top 3 indicators
        top_3 = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
        top_3_names = [ind for ind, _ in top_3]
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "stock_ticker": stock_ticker,
            "model_metrics": metrics,
            "indicator_rankings": [
                {
                    "rank": rank + 1,
                    "indicator": ind,
                    "importance": importance,
                    "correlation": correlations.get(ind, 0.0)
                }
                for rank, (ind, importance) in enumerate(
                    sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
                )
            ],
            "top_3_indicators": top_3_names,
            "insights": insights,
            "recommendations": recommendations,
        }
        
        return report
    
    def save_report(
        self,
        report: Dict[str, Any],
        report_name: str = None
    ) -> Dict[str, str]:
        """Save report to JSON and markdown files
        
        Args:
            report: Report dictionary
            report_name: Name for report file (without extension)
        
        Returns:
            Dictionary with paths to saved files
        """
        if report_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ticker = report.get("stock_ticker", "unknown")
            report_name = f"report_{ticker}_{timestamp}"
        
        # Save JSON report
        json_path = self.report_dir / f"{report_name}.json"
        with open(json_path, "w") as f:
            json.dump(report, f, indent=2)
        
        # Save markdown report
        text_report = self.generate_text_report(report)
        md_path = self.report_dir / f"{report_name}.md"
        with open(md_path, "w") as f:
            f.write(text_report)
        
        # Save text report
        txt_path = self.report_dir / f"{report_name}.txt"
        with open(txt_path, "w") as f:
            f.write(text_report)
        
        return {
            "json": str(json_path),
            "markdown": str(md_path),
            "text": str(txt_path),
        }
    
    def generate_text_report(self, report: Dict[str, Any]) -> str:
        """Generate human-readable text report
        
        Args:
            report: Report dictionary
        
        Returns:
            Formatted text report
        """
        lines = []
        
        lines.append("=" * 80)
        lines.append("TRADING INDICATOR ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append("")
        
        # Header
        lines.append(f"Stock Ticker: {report['stock_ticker']}")
        lines.append(f"Generated: {report['timestamp']}")
        lines.append("")
        
        # Model Metrics
        lines.append("MODEL PERFORMANCE METRICS")
        lines.append("-" * 40)
        metrics = report["model_metrics"]
        lines.append(f"Accuracy:  {metrics.get('accuracy', 0):.4f}")
        lines.append(f"Precision: {metrics.get('precision', 0):.4f}")
        lines.append(f"Recall:    {metrics.get('recall', 0):.4f}")
        lines.append(f"F1-Score:  {metrics.get('f1_score', 0):.4f}")
        if "roc_auc" in metrics:
            lines.append(f"ROC-AUC:   {metrics['roc_auc']:.4f}")
        lines.append("")
        
        # Top Indicators
        lines.append("TOP 3 MOST PREDICTIVE INDICATORS")
        lines.append("-" * 40)
        for i, indicator in enumerate(report["top_3_indicators"], 1):
            lines.append(f"{i}. {indicator}")
        lines.append("")
        
        # Indicator Rankings
        lines.append("INDICATOR RANKINGS (by importance)")
        lines.append("-" * 40)
        for ranking in report["indicator_rankings"]:
            lines.append(
                f"{ranking['rank']:2d}. {ranking['indicator']:20s} "
                f"Importance: {ranking['importance']:.4f}  "
                f"Correlation: {ranking['correlation']:.4f}"
            )
        lines.append("")
        
        # Insights
        lines.append("KEY INSIGHTS")
        lines.append("-" * 40)
        for insight in report["insights"]:
            lines.append(f"• {insight}")
        lines.append("")
        
        # Recommendations
        if report["recommendations"]:
            lines.append("RECOMMENDATIONS")
            lines.append("-" * 40)
            for rec in report["recommendations"]:
                lines.append(f"• {rec}")
            lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
