---
inclusion: manual
---

# Trading Indicator Analysis - Development Steering

## Project Overview

This project analyzes the predictive power of technical trading indicators using machine learning. The system calculates 8 indicators from real stock data, trains a Random Forest model, and identifies which indicators are most effective for price prediction.

## Key Technologies

- **Data Source**: Yahoo Finance (yfinance library)
- **ML Framework**: scikit-learn (Random Forest)
- **GPU Acceleration**: MPS (Metal Performance Shaders) on macOS
- **Data Processing**: pandas, numpy
- **Testing**: pytest, hypothesis (property-based testing)
- **Visualization**: matplotlib, seaborn

## Development Approach

### 1. Incremental Implementation
- Start with data loading and validation (Task 1-2)
- Build indicator calculation layer (Task 3)
- Implement feature engineering (Task 4)
- Train and evaluate model (Task 6-7)
- Add comprehensive testing (Task 11-12)

### 2. Checkpoints
- **Checkpoint 1** (after Task 5): Verify data pipeline works end-to-end
- **Checkpoint 2** (after Task 10): Ensure all components integrate correctly
- **Checkpoint 3** (after Task 13): All tests pass with >85% coverage

### 3. Testing Strategy
- **Unit Tests**: Validate specific examples and edge cases
- **Property-Based Tests**: Validate universal properties across many inputs
- **Minimum Iterations**: 100 per property test
- **Coverage Target**: >85%

## Technical Decisions

### Timeframe
- **1-minute candlesticks**: Provides granular data for accurate indicator calculation
- All calculations and predictions operate on 1-minute intervals

### Indicators Selected
1. **ATR** (14): Volatility measure
2. **SMA** (20, 50): Trend following
3. **Bollinger Bands** (20, 2): Volatility and support/resistance
4. **RSI** (14): Momentum and overbought/oversold
5. **MACD** (12, 26, 9): Trend and momentum
6. **Stochastic** (14, 3): Momentum and reversal signals
7. **ADX** (14): Trend strength
8. **CCI** (20): Cyclical patterns

### Label Definition
- **"up"**: Next day close > current close × 1.005 (0.5% threshold)
- **"down"**: Otherwise
- Threshold chosen to filter noise and focus on meaningful price movements

### Data Split
- **Train**: 70% (oldest data)
- **Validation**: 15%
- **Test**: 15% (newest data)
- **Temporal ordering preserved** to prevent data leakage

### Model Configuration
- **Algorithm**: Random Forest
- **Default Trees**: 100 (configurable)
- **GPU**: MPS on macOS when available, CPU fallback
- **Feature Importance**: Computed during training

## Correctness Properties

The system validates 8 correctness properties through property-based testing:

1. **Indicator Calculation Consistency**: Same data → identical results
2. **Feature Normalization Invertibility**: Normalize → inverse → recover original
3. **Data Split Temporal Integrity**: Train < Validation < Test (strict ordering)
4. **Label Consistency**: Labels match 0.5% threshold rule
5. **Model Prediction Bounds**: Probabilities in [0, 1], sum to 1.0
6. **Feature Importance Completeness**: Importance scores sum to 1.0
7. **Metrics Validity**: Metrics in valid ranges, relationships hold
8. **No Data Leakage**: Test data not used during training

## Error Handling

- **Invalid Ticker**: Descriptive error with format suggestion
- **Insufficient Data**: Error with minimum requirement (500 days)
- **Data Gaps**: Handled via forward-fill or row removal
- **Network Errors**: Retry with exponential backoff, cache fallback
- **Training Failures**: Graceful error with suggestions
- **MPS Unavailable**: Automatic fallback to CPU

## Output Artifacts

- **Trained Model**: Saved to `models/` directory
- **Scaler**: Saved for feature normalization
- **Report**: JSON/markdown with metrics and insights
- **Visualizations**: Feature importance, confusion matrix, ROC curve, correlations
- **Logs**: Detailed execution logs for debugging

## Next Steps

1. Start with Task 1: Set up project structure and dependencies
2. Follow tasks sequentially, using checkpoints to validate progress
3. Run property-based tests to ensure correctness properties hold
4. Review final report to identify most predictive indicators
