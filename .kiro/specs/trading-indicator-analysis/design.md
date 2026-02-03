# Design Document: Trading Indicator Analysis

## Overview

The Trading Indicator Analysis system is a machine learning pipeline that evaluates the predictive power of technical indicators for stock price movements. The system fetches real historical stock data at 1-minute timeframe granularity, calculates eight technical indicators (ATR, SMA, Bollinger Bands, RSI, MACD, Stochastic Oscillator, ADX, CCI), prepares features for model training, trains a Random Forest model, and generates comprehensive performance analysis. The system leverages MPS GPU acceleration on macOS for efficient computation.

**Timeframe Specification**: All candlestick data represents 1-minute periods. Each candle contains Open, High, Low, Close, and Volume data for a 1-minute trading interval. Indicator calculations and price predictions operate on this 1-minute timeframe.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Trading Indicator Analysis                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌───────▼────────┐   │   ┌─────────▼────────┐
        │  Data Layer    │   │   │  Indicator Layer │
        ├────────────────┤   │   ├──────────────────┤
        │ • Data Loader  │   │   │ • ATR Calculator │
        │ • Validator    │   │   │ • SMA Calculator │
        │ • Cache Mgr    │   │   │ • BB Calculator  │
        └────────────────┘   │   │ • RSI Calculator │
                             │   │ • MACD Calculator│
                             │   │ • Stoch Calc     │
                             │   │ • ADX Calculator │
                             │   │ • CCI Calculator │
                             │   └──────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Feature Layer   │
                    ├─────────────────┤
                    │ • Normalizer    │
                    │ • Label Creator │
                    │ • Data Splitter │
                    │ • Balancer      │
                    └─────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Model Layer    │
                    ├─────────────────┤
                    │ • RF Trainer    │
                    │ • Predictor     │
                    │ • Serializer    │
                    └─────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Evaluation Layer│
                    ├─────────────────┤
                    │ • Metrics Calc  │
                    │ • Analyzer      │
                    │ • Reporter      │
                    │ • Visualizer    │
                    └─────────────────┘
```

## Components and Interfaces

### 1. Data Layer

**DataLoader**
- Fetches historical OHLCV data from Yahoo Finance or similar source
- Validates data completeness (minimum 500 trading days)
- Returns pandas DataFrame with columns: Date, Open, High, Low, Close, Volume

**DataValidator**
- Checks for null values, data gaps, and anomalies
- Ensures temporal ordering and consistency
- Raises descriptive errors for invalid data

**CacheManager**
- Caches downloaded data locally to avoid redundant API calls
- Manages cache expiration and updates

### 2. Indicator Layer

Each indicator calculator follows a consistent interface:
- Input: DataFrame with OHLCV data
- Output: DataFrame with original data plus calculated indicator columns
- Handles NaN values through forward-fill or row removal

**IndicatorCalculators**
- ATRCalculator: Computes Average True Range (period=14)
- SMACalculator: Computes Simple Moving Averages (periods=20, 50)
- BollingerBandsCalculator: Computes upper, middle, lower bands (period=20, std=2)
- RSICalculator: Computes Relative Strength Index (period=14)
- MACDCalculator: Computes MACD line, signal line, histogram (12, 26, 9)
- StochasticCalculator: Computes %K and %D (period=14, smoothing=3)
- ADXCalculator: Computes Average Directional Index (period=14)
- CCICalculator: Computes Commodity Channel Index (period=20)

### 3. Feature Layer

**FeatureNormalizer**
- Applies StandardScaler to normalize indicator values
- Stores scaler for later use on test data
- Handles edge cases (constant features, division by zero)

**LabelCreator**
- Creates binary labels: "up" if next day close > current close * 1.005, else "down"
- Handles edge cases at end of dataset
- Returns balanced or imbalanced labels based on data

**DataSplitter**
- Splits data into train (70%), validation (15%), test (15%)
- Preserves temporal ordering (no shuffling)
- Prevents data leakage

**ClassBalancer**
- Detects class imbalance in labels
- Applies SMOTE or class weights if needed
- Logs balancing decisions

### 4. Model Layer

**RandomForestTrainer**
- Initializes Random Forest with configurable parameters (default: 100 trees)
- Trains on normalized features and labels
- Utilizes MPS GPU acceleration when available on macOS
- Computes feature importance during training
- Saves model and metadata to disk

**Predictor**
- Loads trained model
- Makes predictions on new data
- Returns prediction probabilities

**ModelSerializer**
- Saves trained model to pickle/joblib format
- Saves scaler and metadata
- Enables model versioning

### 5. Evaluation Layer

**MetricsCalculator**
- Computes accuracy, precision, recall, F1-score
- Generates confusion matrix
- Computes ROC-AUC score
- Calculates per-class metrics

**IndicatorAnalyzer**
- Ranks indicators by feature importance
- Computes correlation between indicators and price movements
- Identifies top indicator combinations
- Generates actionable insights

**ReportGenerator**
- Aggregates all metrics and analysis
- Creates structured report with findings
- Identifies top 3 most important indicators

**Visualizer**
- Creates feature importance plots
- Generates confusion matrix heatmaps
- Plots ROC curves
- Creates indicator correlation matrices

## Data Models

### Stock Data
```
{
  date: datetime,
  open: float,
  high: float,
  low: float,
  close: float,
  volume: int,
  
  # Indicators
  atr: float,
  sma_20: float,
  sma_50: float,
  bb_upper: float,
  bb_middle: float,
  bb_lower: float,
  rsi: float,
  macd: float,
  macd_signal: float,
  macd_histogram: float,
  stoch_k: float,
  stoch_d: float,
  adx: float,
  cci: float,
  
  # Label
  label: "up" | "down"
}
```

### Model Metadata
```
{
  model_type: "RandomForest",
  n_trees: int,
  training_date: datetime,
  stock_ticker: string,
  data_period: {start_date, end_date},
  train_size: int,
  val_size: int,
  test_size: int,
  feature_names: [string],
  feature_importance: {feature_name: float},
  metrics: {
    accuracy: float,
    precision: float,
    recall: float,
    f1_score: float,
    roc_auc: float
  }
}
```

### Analysis Report
```
{
  timestamp: datetime,
  stock_ticker: string,
  model_metrics: {...},
  indicator_rankings: [
    {rank: 1, indicator: string, importance: float, correlation: float},
    ...
  ],
  top_3_indicators: [string],
  best_indicator_combinations: [[string]],
  insights: [string],
  recommendations: [string]
}
```

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Indicator Calculation Consistency

*For any* stock price dataset with valid OHLCV data, calculating indicators multiple times on the same data should produce identical results (deterministic computation).

**Validates: Requirements 1.1-1.8**

### Property 2: Feature Normalization Invertibility

*For any* set of indicator values, normalizing them with StandardScaler and then inverse-transforming should recover the original values within floating-point precision.

**Validates: Requirements 2.4**

### Property 3: Data Split Temporal Integrity

*For any* dataset split into train/validation/test sets, all training data timestamps should be strictly before all validation data timestamps, which should be strictly before all test data timestamps.

**Validates: Requirements 2.7, 2.8**

### Property 4: Label Consistency

*For any* price sequence, the label "up" should be assigned if and only if the next day's close price is greater than current close price multiplied by 1.005.

**Validates: Requirements 2.6**

### Property 5: Model Prediction Bounds

*For any* trained Random Forest model, all prediction probabilities should be in the range [0, 1] and sum to 1.0 for binary classification.

**Validates: Requirements 3.2, 3.7**

### Property 6: Feature Importance Completeness

*For any* trained Random Forest model, the sum of all feature importance scores should equal 1.0 (or very close due to floating-point precision).

**Validates: Requirements 3.3, 4.4**

### Property 7: Metrics Validity

*For any* set of predictions and labels, computed metrics (accuracy, precision, recall, F1) should satisfy: 0 ≤ metric ≤ 1, and precision + recall should be consistent with F1-score calculation.

**Validates: Requirements 4.1-4.5**

### Property 8: No Data Leakage

*For any* model trained on split data, the model should not have access to test data during training, and predictions on test data should use only information available at training time.

**Validates: Requirements 2.8**

## Error Handling

**Data Loading Errors**
- Invalid ticker: Return error with suggestion to check ticker format
- Insufficient data: Return error with minimum requirement (500 days)
- Network errors: Retry with exponential backoff, cache fallback
- Missing OHLCV columns: Return error listing required columns

**Indicator Calculation Errors**
- NaN propagation: Forward-fill or remove incomplete rows
- Division by zero: Handle gracefully in RSI, Stochastic calculations
- Insufficient data for period: Return error with minimum data requirement

**Model Training Errors**
- Empty features: Return error indicating no valid features
- All same labels: Return error indicating no class variation
- Memory errors: Suggest reducing dataset size or tree count
- MPS unavailable: Gracefully fall back to CPU

**Evaluation Errors**
- Empty predictions: Return error indicating no predictions made
- Mismatched shapes: Return error with dimension information

## Testing Strategy

### Unit Testing

Unit tests validate specific examples, edge cases, and error conditions:

1. **Data Loading Tests**
   - Valid ticker returns data with correct shape
   - Invalid ticker raises appropriate error
   - Insufficient data raises error with minimum requirement
   - Missing columns detected and reported

2. **Indicator Calculation Tests**
   - Each indicator produces expected values for known inputs
   - NaN handling works correctly (forward-fill, removal)
   - Edge cases (first rows, last rows) handled properly
   - Indicator values within expected ranges

3. **Feature Engineering Tests**
   - Normalization preserves data shape
   - Labels created correctly based on price threshold
   - Data split maintains temporal ordering
   - No data leakage between splits

4. **Model Training Tests**
   - Model trains without errors on valid data
   - Feature importance scores sum to 1.0
   - Model saves and loads correctly
   - Predictions have correct shape and bounds

5. **Evaluation Tests**
   - Metrics calculated correctly for known predictions
   - Confusion matrix dimensions correct
   - Feature importance rankings valid
   - Report generation completes without errors

### Property-Based Testing

Property-based tests validate universal properties across many generated inputs:

1. **Property 1: Indicator Calculation Consistency**
   - Generate random OHLCV data
   - Calculate indicators twice
   - Assert results are identical
   - Minimum 100 iterations

2. **Property 2: Feature Normalization Invertibility**
   - Generate random indicator values
   - Normalize and inverse-transform
   - Assert recovery within floating-point tolerance
   - Minimum 100 iterations

3. **Property 3: Data Split Temporal Integrity**
   - Generate random timestamps
   - Split into train/val/test
   - Assert strict temporal ordering
   - Minimum 100 iterations

4. **Property 4: Label Consistency**
   - Generate random price sequences
   - Create labels based on threshold
   - Verify label correctness for all rows
   - Minimum 100 iterations

5. **Property 5: Model Prediction Bounds**
   - Train model on random data
   - Generate predictions
   - Assert all probabilities in [0, 1]
   - Assert probabilities sum to 1.0
   - Minimum 100 iterations

6. **Property 6: Feature Importance Completeness**
   - Train model on random data
   - Extract feature importance
   - Assert sum equals 1.0 (within tolerance)
   - Minimum 100 iterations

7. **Property 7: Metrics Validity**
   - Generate random predictions and labels
   - Calculate metrics
   - Assert all metrics in valid ranges
   - Assert metric relationships hold
   - Minimum 100 iterations

8. **Property 8: No Data Leakage**
   - Train model on split data
   - Verify test data not used during training
   - Verify predictions use only training-time information
   - Minimum 100 iterations

### Testing Configuration

- **Framework**: pytest with pytest-randomly for property-based testing
- **Property Testing Library**: hypothesis for Python
- **Minimum Iterations**: 100 per property test
- **Coverage Target**: >85% code coverage
- **CI/CD Integration**: Run all tests on every commit
