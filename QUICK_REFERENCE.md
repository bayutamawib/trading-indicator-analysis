# Quick Reference Guide

## Installation (2 minutes)

```bash
# Clone and setup
git clone https://github.com/yourusername/trading-indicator-analysis.git
cd trading-indicator-analysis
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Basic Usage

```bash
# Analyze a stock
python src/main.py analyze --ticker AAPL

# With custom dates
python src/main.py analyze --ticker AAPL --start 2022-01-01 --end 2024-02-01

# Different interval
python src/main.py analyze --ticker GOOGL --interval 1d
```

## Output Files

```
reports/
├── report_AAPL_20260203_224049.md      # Human-readable report
├── report_AAPL_20260203_224049.txt     # Text format
├── report_AAPL_20260203_224049.json    # JSON format
└── visualizations/
    ├── feature_importance.png
    ├── confusion_matrix.png
    ├── roc_curve.png
    └── indicator_correlation.png

models/
└── model_20260203_224049/
    ├── model.joblib                    # Trained model
    ├── scaler.joblib                   # Feature scaler
    └── metadata.json                   # Model info
```

## Key Files

| File | Purpose |
|------|---------|
| `src/main.py` | CLI entry point |
| `src/analyzer.py` | Main orchestrator |
| `src/data/loader.py` | Yahoo Finance integration |
| `src/indicators/pipeline.py` | Indicator calculation |
| `src/features/engineer.py` | Feature engineering |
| `src/models/trainer.py` | Model training |
| `src/evaluation/evaluator.py` | Evaluation & reporting |

## 8 Technical Indicators

1. **ATR** - Volatility (period=14)
2. **SMA** - Trend (periods=20, 50)
3. **Bollinger Bands** - Volatility (period=20, std=2)
4. **RSI** - Momentum (period=14)
5. **MACD** - Trend (12, 26, 9)
6. **Stochastic** - Momentum (period=14, smoothing=3)
7. **ADX** - Trend strength (period=14)
8. **CCI** - Cycles (period=20)

## Model Configuration

- **Algorithm**: Random Forest
- **Trees**: 100 (configurable)
- **GPU**: MPS on macOS (auto-detected)
- **Features**: 14 (8 indicators + variations)
- **Label**: Binary (up/down at 0.5% threshold)
- **Split**: 70% train, 15% val, 15% test

## Test Results

| Stock | Accuracy | Top Indicator |
|-------|----------|---|
| AAPL | 71.9% | Stoch_K |
| GOOGL | 63.2% | Stoch_K |

## Common Commands

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src tests/

# Analyze multiple stocks
for ticker in AAPL GOOGL MSFT; do
    python src/main.py analyze --ticker $ticker
done

# Clear cache
rm -rf data/cache/*

# Check GPU support
python -c "from src.models.gpu import GPUAccelerator; print(GPUAccelerator.get_device_info())"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named 'yfinance'" | `pip install -r requirements.txt` |
| "Invalid ticker" | Check ticker on Yahoo Finance |
| "Insufficient data" | Use longer date range (500+ days) |
| "No data found" | Check internet, verify ticker |
| Slow first run | First run downloads data; cache speeds up subsequent runs |

## Project Structure

```
src/
├── main.py              # CLI
├── analyzer.py          # Orchestrator
├── data/                # Data loading
├── indicators/          # 8 indicators
├── features/            # Feature engineering
├── models/              # Model training
└── evaluation/          # Evaluation & reporting

specs/
├── requirements.md      # 6 requirements
├── design.md           # Architecture
└── tasks.md            # Implementation status

tests/
├── conftest.py         # Fixtures
└── test_pipeline_checkpoint.py

reports/                # Generated reports
models/                 # Trained models
data/cache/             # Cached stock data
```

## Documentation

- **README.md** - Project overview and features
- **SETUP.md** - Installation and setup guide
- **QUICK_REFERENCE.md** - This file
- **GITHUB_READY.md** - GitHub deployment checklist
- **specs/requirements.md** - Detailed requirements
- **specs/design.md** - System architecture
- **specs/tasks.md** - Implementation tasks

## Key Metrics

- **Accuracy**: Percentage of correct predictions
- **Precision**: True positives / (true positives + false positives)
- **Recall**: True positives / (true positives + false negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under ROC curve (0.5 = random, 1.0 = perfect)

## Data Requirements

- **Minimum**: 500 trading days
- **Format**: OHLCV (Open, High, Low, Close, Volume)
- **Source**: Yahoo Finance
- **Caching**: Automatic local caching

## Label Definition

```
Label = "up" if next_close > current_close * 1.005
Label = "down" otherwise
```

Threshold: 0.5% price change

## Feature Normalization

- **Method**: StandardScaler
- **Mean**: 0
- **Std Dev**: 1
- **Invertible**: Yes (for reverse transformation)

## Report Contents

1. **Model Metrics**
   - Accuracy, Precision, Recall, F1-Score, ROC-AUC

2. **Indicator Rankings**
   - Feature importance scores
   - Correlation with price movements

3. **Top 3 Indicators**
   - Most predictive indicators

4. **Insights**
   - Key findings from analysis

5. **Recommendations**
   - Actionable suggestions

## Supported Intervals

- `1m` - 1-minute
- `5m` - 5-minute
- `15m` - 15-minute
- `1h` - 1-hour
- `1d` - 1-day (default)

## Date Format

Use `YYYY-MM-DD`:
- Example: `2024-02-03`
- Default start: 1 year ago
- Default end: Today

## Performance Tips

1. Use `1d` interval for faster analysis
2. Reuse cached data (first run is slowest)
3. Use GPU on macOS (automatic)
4. Smaller date ranges train faster

## Getting Help

1. Check README.md
2. Check SETUP.md
3. Review specs/ directory
4. Open GitHub issue
5. Check existing issues

## License

MIT License - See LICENSE file

---

**Quick Start**: `python src/main.py analyze --ticker AAPL`

**Documentation**: See README.md and SETUP.md

**Specifications**: See specs/ directory
