# Setup Guide

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- macOS (for MPS GPU acceleration) or Linux/Windows (CPU only)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/trading-indicator-analysis.git
cd trading-indicator-analysis
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Test the installation
python -c "import pandas; import sklearn; import yfinance; print('All dependencies installed successfully!')"
```

## Quick Start

### Run Your First Analysis

```bash
# Analyze Apple stock (AAPL) for the last year
python src/main.py analyze --ticker AAPL

# Analyze with custom date range
python src/main.py analyze --ticker AAPL --start 2022-01-01 --end 2024-02-01

# Analyze with different interval
python src/main.py analyze --ticker GOOGL --start 2023-01-01 --end 2024-01-01 --interval 1d
```

### View Results

After running an analysis, check:
- **Reports**: `reports/report_[TICKER]_[TIMESTAMP].md` (human-readable)
- **Visualizations**: `reports/visualizations/` (charts and graphs)
- **Models**: `models/model_[TIMESTAMP]/` (trained model files)

## Project Structure

```
trading-indicator-analysis/
├── src/                    # Source code
│   ├── main.py            # CLI entry point
│   ├── analyzer.py        # Main orchestrator
│   ├── data/              # Data loading & validation
│   ├── indicators/        # Technical indicators
│   ├── features/          # Feature engineering
│   ├── models/            # Model training
│   └── evaluation/        # Evaluation & reporting
├── tests/                 # Test suite
├── specs/                 # Specification documents
├── data/                  # Data storage (auto-created)
├── models/                # Trained models (auto-created)
├── reports/               # Analysis reports (auto-created)
├── requirements.txt       # Python dependencies
├── README.md             # Project overview
└── SETUP.md              # This file
```

## Configuration

### Supported Stock Tickers

Any valid stock ticker symbol supported by Yahoo Finance:
- US Stocks: AAPL, GOOGL, MSFT, AMZN, TSLA, etc.
- International: 0001.HK (Hong Kong), 6758.T (Japan), etc.

### Supported Intervals

- `1m` - 1-minute candlesticks
- `5m` - 5-minute candlesticks
- `15m` - 15-minute candlesticks
- `1h` - 1-hour candlesticks
- `1d` - 1-day candlesticks (default)

### Date Format

Use `YYYY-MM-DD` format for dates:
- Example: `2024-02-03`
- Default start: 1 year ago
- Default end: Today

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_pipeline_checkpoint.py -v

# Run tests matching a pattern
pytest -k "indicator" -v
```

## Troubleshooting

### Issue: "No module named 'yfinance'"

**Solution**: Make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Invalid ticker 'XXXX'"

**Solution**: Verify the ticker symbol is correct. Check Yahoo Finance for valid symbols.

### Issue: "Insufficient data: X rows found, minimum 500 trading days required"

**Solution**: Use a longer date range. The system requires at least 500 trading days of data.

### Issue: "No data found for ticker"

**Solution**: 
- Check internet connection
- Verify ticker symbol is correct
- Try a different date range
- Check if the stock is available on Yahoo Finance

### Issue: Slow performance on first run

**Solution**: The first run downloads data from Yahoo Finance. Subsequent runs use cached data, which is much faster.

## GPU Acceleration (macOS)

The system automatically detects and uses MPS (Metal Performance Shaders) on macOS:

```bash
# Check if MPS is available
python -c "from src.models.gpu import GPUAccelerator; print(GPUAccelerator.get_device_info())"
```

Output example:
```
{'platform': 'Darwin', 'mps_available': True, 'device': 'MPS'}
```

## Output Files

### Reports

Generated in `reports/` directory:
- `report_[TICKER]_[TIMESTAMP].md` - Markdown format (human-readable)
- `report_[TICKER]_[TIMESTAMP].txt` - Text format
- `report_[TICKER]_[TIMESTAMP].json` - JSON format (programmatic use)

### Visualizations

Generated in `reports/visualizations/`:
- `feature_importance.png` - Bar chart of indicator importance
- `confusion_matrix.png` - Heatmap of prediction accuracy
- `roc_curve.png` - ROC curve for model evaluation
- `indicator_correlation.png` - Correlation with price movements

### Models

Generated in `models/model_[TIMESTAMP]/`:
- `model.joblib` - Trained Random Forest model
- `scaler.joblib` - Feature normalization scaler
- `metadata.json` - Model parameters and metrics

## Data Caching

Downloaded stock data is cached locally in `data/cache/` to avoid redundant API calls:
- Cache format: `[TICKER]_[START_DATE]_[END_DATE].pkl`
- Cache is automatically used on subsequent runs
- To clear cache: `rm -rf data/cache/*`

## Advanced Usage

### Analyze Multiple Stocks

```bash
# Create a script to analyze multiple stocks
for ticker in AAPL GOOGL MSFT AMZN TSLA; do
    python src/main.py analyze --ticker $ticker --start 2022-01-01 --end 2024-02-01
done
```

### Custom Analysis

Modify `src/analyzer.py` to customize the analysis pipeline:
- Change indicator parameters
- Adjust label threshold
- Modify data split ratios
- Use different ML models

## Performance Tips

1. **Use longer intervals for faster analysis**: `--interval 1d` is faster than `--interval 1m`
2. **Reuse cached data**: First run downloads data, subsequent runs use cache
3. **Use GPU acceleration**: Automatic on macOS with MPS
4. **Reduce date range**: Smaller datasets train faster

## Next Steps

1. Read `specs/trading-indicator-analysis/requirements.md` for detailed requirements
2. Check `specs/trading-indicator-analysis/design.md` for architecture details
3. Review `specs/trading-indicator-analysis/tasks.md` for implementation status
4. Explore the generated reports and visualizations

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the specification documents in `specs/`
3. Open an issue on GitHub
4. Check existing issues for similar problems

## License

This project is licensed under the MIT License.

---

**Happy analyzing!** 📊
