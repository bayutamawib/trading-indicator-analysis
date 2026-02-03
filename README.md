# Trading Indicator Analysis

A production-ready machine learning system that analyzes the performance of technical trading indicators for stock price prediction using Random Forest models. Features MLflow model registry, Streamlit web UI, Docker containerization, and Kubernetes deployment support.

## 🎯 Overview

This project evaluates which technical indicators are most predictive of stock price movements. It fetches real historical data from Yahoo Finance, calculates 8 different technical indicators, trains a Random Forest model, and provides comprehensive analysis with visualizations.

**Key Finding**: Stochastic Oscillator (Stoch_K), MACD Histogram, and ATR are consistently the most predictive indicators across different stocks.

## ✨ Features

- **8 Technical Indicators**: ATR, SMA, Bollinger Bands, RSI, MACD, Stochastic Oscillator, ADX, CCI
- **Real Stock Data**: Fetches historical data from Yahoo Finance with local caching
- **Random Forest Model**: Trains on indicator features to predict price movements
- **GPU Acceleration**: MPS (Metal Performance Shaders) support on macOS
- **Comprehensive Evaluation**: Accuracy, precision, recall, F1-score, ROC-AUC metrics
- **Feature Importance Analysis**: Identifies most predictive indicators
- **MLflow Model Registry**: Track, manage, and version all trained models
- **Streamlit Web UI**: Interactive web interface for running analyses and comparing models
- **Automated Reporting**: Generates JSON, Markdown, and text reports
- **Visualizations**: Feature importance, confusion matrix, ROC curve, indicator correlations
- **Docker Support**: Containerized deployment with Docker
- **Kubernetes Ready**: Helm charts and manifests for Kubernetes deployment

## 📊 Test Results

| Stock | Accuracy | Top Indicators | Model |
|-------|----------|---|---|
| AAPL | 71.9% | Stoch_K, MACD_Histogram, ATR | Random Forest |
| GOOGL | 63.2% | Stoch_K, ADX, MACD_Histogram | Random Forest |

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/trading-indicator-analysis.git
cd trading-indicator-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### CLI Analysis
```bash
# Analyze a stock (default: last 1 year)
python src/main.py analyze --ticker AAPL

# Analyze with custom date range
python src/main.py analyze --ticker AAPL --start 2022-01-01 --end 2024-02-01

# Analyze with different interval
python src/main.py analyze --ticker GOOGL --start 2023-01-01 --end 2024-01-01 --interval 1d
```

#### Streamlit Web UI
```bash
# Start the web interface
streamlit run app.py

# Access at http://localhost:8501
```

#### MLflow UI
```bash
# View model registry and experiments
mlflow ui

# Access at http://localhost:5000
```

#### Docker
```bash
# Build Docker image
docker build -t trading-indicator-analysis .

# Run container
docker run -p 8501:8501 -p 5000:5000 trading-indicator-analysis

# Access Streamlit at http://localhost:8501
# Access MLflow at http://localhost:5000
```

#### Kubernetes
```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Port forward to access services
kubectl port-forward svc/streamlit-service 8501:8501
kubectl port-forward svc/mlflow-service 5000:5000

# Access Streamlit at http://localhost:8501
# Access MLflow at http://localhost:5000
```

### Output

The system generates:
- **Reports**: `reports/report_[TICKER]_[TIMESTAMP].{json,md,txt}`
- **Visualizations**: `reports/visualizations/`
- **Models**: `models/model_[TIMESTAMP]/`
- **MLflow Registry**: `mlruns/` directory with all model tracking

## 📁 Project Structure

```
trading-indicator-analysis/
├── src/                           # Source code
│   ├── main.py                   # CLI entry point
│   ├── analyzer.py               # Main orchestrator
│   ├── data/                     # Data loading & validation
│   ├── indicators/               # Technical indicators
│   ├── features/                 # Feature engineering
│   ├── models/                   # Model training
│   │   ├── mlflow_registry.py   # MLflow integration
│   │   └── ...
│   └── evaluation/               # Evaluation & reporting
├── app.py                        # Streamlit web UI
├── tests/                        # Test suite
├── specs/                        # Specification documents
├── docker/                       # Docker configuration
│   ├── Dockerfile               # Docker image definition
│   └── docker-compose.yml       # Multi-container setup
├── k8s/                         # Kubernetes manifests
│   ├── deployment.yaml          # Kubernetes deployment
│   ├── service.yaml             # Kubernetes service
│   └── helm/                    # Helm charts
├── data/                        # Data storage
├── models/                      # Trained models
├── mlruns/                      # MLflow tracking
├── reports/                     # Analysis reports
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 Technical Details

- **Language**: Python 3.11+
- **ML Framework**: scikit-learn
- **Data Source**: Yahoo Finance (yfinance)
- **Model Registry**: MLflow
- **Web UI**: Streamlit
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **GPU**: MPS (Metal Performance Shaders) on macOS

## 📈 Indicators Analyzed

1. **ATR** - Volatility measure
2. **SMA** - Trend following (20, 50 periods)
3. **Bollinger Bands** - Volatility and support/resistance
4. **RSI** - Momentum and overbought/oversold
5. **MACD** - Trend and momentum
6. **Stochastic Oscillator** - Momentum and reversal signals
7. **ADX** - Trend strength
8. **CCI** - Cyclical patterns

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Yahoo Finance for stock data
- scikit-learn for ML algorithms
- MLflow for model tracking
- Streamlit for web UI
- Docker and Kubernetes communities

---

**Note**: This project is for educational and research purposes.
