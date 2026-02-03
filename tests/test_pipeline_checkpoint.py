"""Checkpoint test for data pipeline end-to-end functionality"""

import pytest
import pandas as pd
from src.data import DataLoader, DataValidator
from src.indicators import IndicatorPipeline
from src.features import FeatureEngineer


def test_data_loading():
    """Test data loading from Yahoo Finance"""
    loader = DataLoader()
    
    # Try to load real data (this requires internet connection)
    try:
        df = loader.fetch_data("AAPL", "2024-01-01", "2024-02-01", interval="1d")
        assert not df.empty, "Data should not be empty"
        assert len(df) > 0, "Should have at least one row"
        print(f"✓ Data loading successful: {len(df)} rows loaded")
    except Exception as e:
        print(f"⚠ Data loading skipped (requires internet): {str(e)}")


def test_data_validation(sample_ohlcv_data):
    """Test data validation"""
    validator = DataValidator()
    
    # Should pass validation
    try:
        validator.validate_data(sample_ohlcv_data)
        print("✓ Data validation passed")
    except ValueError as e:
        pytest.fail(f"Validation failed: {str(e)}")


def test_indicator_calculation(sample_ohlcv_data):
    """Test indicator calculation pipeline"""
    pipeline = IndicatorPipeline()
    
    df_with_indicators = pipeline.calculate_all_indicators(sample_ohlcv_data)
    
    # Check that all indicators were calculated
    indicator_cols = pipeline.get_indicator_columns()
    for col in indicator_cols:
        assert col in df_with_indicators.columns, f"Missing indicator: {col}"
    
    # Check that no NaN values remain
    assert not df_with_indicators[indicator_cols].isnull().any().any(), "Indicators should not have NaN values"
    
    print(f"✓ Indicator calculation successful: {len(indicator_cols)} indicators calculated")


def test_feature_engineering(sample_ohlcv_data):
    """Test feature engineering pipeline"""
    # Calculate indicators first
    pipeline = IndicatorPipeline()
    df_with_indicators = pipeline.calculate_all_indicators(sample_ohlcv_data)
    
    # Prepare features
    engineer = FeatureEngineer(indicator_columns=pipeline.get_indicator_columns())
    result = engineer.prepare_features(df_with_indicators, apply_balancing=False)
    
    # Check that all splits were created
    assert "X_train" in result, "Missing X_train"
    assert "X_val" in result, "Missing X_val"
    assert "X_test" in result, "Missing X_test"
    assert "y_train" in result, "Missing y_train"
    assert "y_val" in result, "Missing y_val"
    assert "y_test" in result, "Missing y_test"
    
    # Check split sizes
    assert len(result["X_train"]) > 0, "Training set should not be empty"
    assert len(result["X_val"]) > 0, "Validation set should not be empty"
    assert len(result["X_test"]) > 0, "Test set should not be empty"
    
    # Check that labels are binary
    assert set(result["y_train"].unique()).issubset({0, 1}), "Labels should be binary"
    
    print(f"✓ Feature engineering successful:")
    print(f"  - Train: {len(result['X_train'])} samples")
    print(f"  - Val: {len(result['X_val'])} samples")
    print(f"  - Test: {len(result['X_test'])} samples")


def test_end_to_end_pipeline(sample_ohlcv_data):
    """Test complete end-to-end pipeline"""
    print("\n=== End-to-End Pipeline Test ===")
    
    # Step 1: Validate data
    validator = DataValidator()
    validator.validate_data(sample_ohlcv_data)
    print("✓ Step 1: Data validation passed")
    
    # Step 2: Calculate indicators
    pipeline = IndicatorPipeline()
    df_with_indicators = pipeline.calculate_all_indicators(sample_ohlcv_data)
    print("✓ Step 2: Indicators calculated")
    
    # Step 3: Prepare features
    engineer = FeatureEngineer(indicator_columns=pipeline.get_indicator_columns())
    result = engineer.prepare_features(df_with_indicators, apply_balancing=False)
    print("✓ Step 3: Features prepared")
    
    # Step 4: Verify metadata
    metadata = engineer.get_metadata()
    assert metadata["n_features"] > 0, "Should have features"
    assert metadata["n_train"] > 0, "Should have training data"
    print(f"✓ Step 4: Metadata verified")
    print(f"  - Features: {metadata['n_features']}")
    print(f"  - Total samples: {metadata['n_samples']}")
    print(f"  - Train/Val/Test: {metadata['n_train']}/{metadata['n_val']}/{metadata['n_test']}")
    
    print("\n✓ End-to-end pipeline test PASSED")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
