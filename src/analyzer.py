"""Main trading indicator analyzer orchestrator"""

import logging
from datetime import datetime

from src.data import DataLoader, DataValidator
from src.indicators import IndicatorPipeline
from src.features import FeatureEngineer
from src.models import ModelTrainer
from src.evaluation import Evaluator

logger = logging.getLogger(__name__)


class TradingIndicatorAnalyzer:
    """Main orchestrator for trading indicator analysis"""
    
    def __init__(self):
        """Initialize analyzer with all components"""
        self.data_loader = DataLoader()
        self.data_validator = DataValidator()
        self.indicator_pipeline = IndicatorPipeline()
        self.feature_engineer = FeatureEngineer()
        self.model_trainer = ModelTrainer()
        self.evaluator = Evaluator()
    
    def analyze(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        interval: str = "1d"
    ) -> dict:
        """Analyze trading indicators for a stock
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Candlestick interval (default: 1d)
        
        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Starting analysis for {ticker} from {start_date} to {end_date}")
        
        try:
            # Step 1: Load data
            logger.info("Step 1: Loading data...")
            df = self.data_loader.fetch_data(ticker, start_date, end_date, interval=interval)
            logger.info(f"Loaded {len(df)} rows of data")
            
            # Step 2: Validate data
            logger.info("Step 2: Validating data...")
            self.data_validator.validate_data(df)
            logger.info("Data validation passed")
            
            # Step 3: Calculate indicators
            logger.info("Step 3: Calculating indicators...")
            df_with_indicators = self.indicator_pipeline.calculate_all_indicators(df)
            logger.info(f"Calculated {len(self.indicator_pipeline.get_indicator_columns())} indicators")
            
            # Step 4: Prepare features
            logger.info("Step 4: Preparing features...")
            self.feature_engineer.indicator_columns = self.indicator_pipeline.get_indicator_columns()
            feature_result = self.feature_engineer.prepare_features(df_with_indicators)
            logger.info(f"Prepared features: {feature_result['metadata']['n_features']} features")
            
            # Step 5: Train model
            logger.info("Step 5: Training model...")
            train_result = self.model_trainer.train_and_save(
                feature_result["X_train"],
                feature_result["y_train"],
                feature_result["X_val"],
                feature_result["y_val"],
                feature_result["normalizer"],
                stock_ticker=ticker,
                class_weights=feature_result["metadata"].get("class_weights")
            )
            logger.info(f"Model trained with validation accuracy: {train_result['validation_accuracy']:.4f}")
            
            # Step 6: Evaluate model
            logger.info("Step 6: Evaluating model...")
            eval_result = self.evaluator.evaluate_model(
                train_result["model"],
                feature_result["X_test"],
                feature_result["y_test"],
                feature_result["X_train"],
                feature_result["y_train"],
                feature_result["metadata"]["feature_names"],
                stock_ticker=ticker
            )
            logger.info(f"Model evaluation complete. Test accuracy: {eval_result['metrics']['accuracy']:.4f}")
            
            # Compile results
            results = {
                "status": "success",
                "ticker": ticker,
                "timestamp": datetime.now().isoformat(),
                "data_info": {
                    "n_samples": len(df),
                    "date_range": f"{start_date} to {end_date}",
                },
                "feature_info": feature_result["metadata"],
                "model_info": train_result["metadata"],
                "evaluation": eval_result,
                "text_report": eval_result["text_report"],
                "report_paths": eval_result.get("report_paths", {}),
            }
            
            logger.info("Analysis complete!")
            return results
        
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "ticker": ticker,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
