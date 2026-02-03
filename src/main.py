"""Main entry point for Trading Indicator Analysis system"""

import argparse
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import TradingIndicatorAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Trading Indicator Analysis - Analyze technical indicators for stock price prediction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py analyze --ticker AAPL
  python src/main.py analyze --ticker GOOGL --start 2023-01-01 --end 2024-01-01
  python src/main.py analyze --ticker MSFT --start 2024-01-01
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze trading indicators for a stock")
    analyze_parser.add_argument("--ticker", required=True, help="Stock ticker symbol (e.g., AAPL)")
    analyze_parser.add_argument(
        "--start",
        default=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
        help="Start date (YYYY-MM-DD, default: 1 year ago)"
    )
    analyze_parser.add_argument(
        "--end",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="End date (YYYY-MM-DD, default: today)"
    )
    analyze_parser.add_argument(
        "--interval",
        default="1d",
        choices=["1m", "5m", "15m", "1h", "1d"],
        help="Candlestick interval (default: 1d)"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "analyze":
        try:
            analyzer = TradingIndicatorAnalyzer()
            results = analyzer.analyze(
                args.ticker,
                args.start,
                args.end,
                interval=args.interval
            )
            
            if results["status"] == "success":
                print("\n" + results["text_report"])
                
                # Display report file paths
                report_paths = results.get("report_paths", {})
                if report_paths:
                    print("\n" + "=" * 80)
                    print("REPORT FILES SAVED")
                    print("=" * 80)
                    if "markdown" in report_paths:
                        print(f"Markdown Report: {report_paths['markdown']}")
                    if "text" in report_paths:
                        print(f"Text Report:     {report_paths['text']}")
                    if "json" in report_paths:
                        print(f"JSON Report:     {report_paths['json']}")
                
                # Display visualization paths
                viz_paths = results.get("evaluation", {}).get("visualizations", {})
                if viz_paths:
                    print("\n" + "=" * 80)
                    print("VISUALIZATIONS SAVED")
                    print("=" * 80)
                    for viz_name, viz_path in viz_paths.items():
                        print(f"{viz_name:25s}: {viz_path}")
            else:
                print(f"Error: {results['error']}")
                sys.exit(1)
        
        except Exception as e:
            logger.error(f"Failed to analyze {args.ticker}: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
