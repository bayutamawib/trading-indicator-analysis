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

**DataLoader** (`src/data/loader.py`)
- Fetches historical OHLCV data from Yahoo Finance
- Validates data completeness (minimum 500 trading days)
- Returns pandas DataFrame with columns: Date, Open, High, Low, Close, Volume
- Implements local caching to avoid redundant API calls

**DataValidator** (`src/data/validator.py`)
- Checks for null values, data gaps, and anomalies
- Ensures temporal ordering and consistency
- Raises descriptive errors for invalid data

### 2. Indicator Layer

**IndicatorCalculators** (`src/indicators/`)
- ATRCalculator: Computes Average True Range (period=14)
- SMACalculator: Computes Simple Moving Averages (periods=20, 50)
- BollingerBandsCalculator: Computes upper, middle, lower bands (period=20, std=2)
- RSICalculator: Computes Relative Strength Index (period=14)
- MACDCalculator: Computes MACD line, signal line, histogram (12, 26, 9)
- StochasticCalculator: Computes %K and %D (period=14, smoothing=3)
- ADXCalculator: Computes Average Directional Index (period=14)
- CCICalculator: Computes Commodity Channel Index (period=20)

**IndicatorPipeline** (`src/indicators/pipeline.py`)
- Orchestrates calculation of all indicators
- Returns DataFrame with original OHLCV plus all indicators

### 3. Feature Layer

**FeatureNormalizer** (`src/features/normalizer.py`)
- Applies StandardScaler to normalize indicator values
- Stores scaler for later use on test data

**LabelCreator** (`src/features/labels.py`)
- Creates binary labels: "up" if next close > current close * 1.005, else "down"

**DataSplitter** (`src/features/splitter.py`)
- Splits data into train (70%), validation (15%), test (15%)
- Preserves temporal ordering (no shuffling)

**ClassBalancer** (`src/features/balancer.py`)
- Detects class imbalance in labels
- Applies SMOTE or class weights if needed

**FeatureEngineer** (`src/features/engineer.py`)
- Orchestrates feature engineering pipeline

### 4. Model Layer

**RandomForestTrainer** (`src/models/trainer.py`)
- Initializes Random Forest with configurable parameters (default: 100 trees)
- Trains on normalized features and labels
- Computes feature importance during training

**GPUAccelerator** (`src/models/gpu.py`)
- Detects MPS availability on macOS
- Configures environment for GPU acceleration

**ModelSerializer** (`src/models/serializer.py`)
- Saves trained model to joblib format
- Saves scaler and metadata

**ModelTrainer** (`src/models/orchestrator.py`)
- Orchestrates model training pipeline

### 5. Evaluation Layer

**MetricsCalculator** (`src/evaluation/metrics.py`)
- Computes accuracy, precision, recall, F1-score
- Generates confusion matrix
- Computes ROC-AUC score

**IndicatorAnalyzer** (`src/evaluation/analyzer.py`)
- Ranks indicators by feature importance
- Computes correlation between indicators and price movements
- Generates actionable insights

**ReportGenerator** (`src/evaluation/reporter.py`)
- Generates comprehensive analysis reports
- Saves reports in JSON, Markdown, and Text formats

**Visualizer** (`src/evaluation/visualizer.py`)
- Creates feature importance plots
- Generates confusion matrix heatmaps
- Plots ROC curves
- Creates indicator correlation matrices

**Evaluator** (`src/evaluation/evaluator.py`)
- Orchestrates evaluation pipeline

## Main Orchestrator

**TradingIndicatorAnalyzer** (`src/analyzer.py`)
- Orchestrates entire analysis pipeline
- Coordinates all components from data loading to reporting

## CLI Interface

**main.py** (`src/main.py`)
- Command-line interface for running analyses
- Usage: `python src/main.py analyze --ticker AAPL --start 2022-01-01 --end 2024-02-01`

## Testing Strategy

### Unit Testing
- Data loading and validation
- Indicator calculations
- Feature engineering
- Model training
- Evaluation and metrics

### Property-Based Testing
- Indicator calculation consistency
- Feature normalization invertibility
- Data split temporal integrity
- Label consistency
- Model prediction bounds
- Feature importance completeness
- Metrics validity
- No data leakage

## Error Handling

- Invalid ticker: Descriptive error with format suggestion
- Insufficient data: Error with minimum requirement (500 days)
- Data gaps: Handled via forward-fill or row removal
- Network errors: Retry with exponential backoff, cache fallback
- Training failures: Graceful error with suggestions
- MPS unavailable: Automatic fallback to CPU
