"""Streamlit web UI for Trading Indicator Analysis"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import logging

from src.analyzer import TradingIndicatorAnalyzer
from src.models.mlflow_registry import MLflowRegistry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Trading Indicator Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "analyzer" not in st.session_state:
    st.session_state.analyzer = TradingIndicatorAnalyzer()

if "mlflow_registry" not in st.session_state:
    st.session_state.mlflow_registry = MLflowRegistry()

if "results" not in st.session_state:
    st.session_state.results = None


def main():
    """Main Streamlit app"""
    
    # Header
    st.title("📈 Trading Indicator Analysis")
    st.markdown("Analyze technical indicators for stock price prediction using Machine Learning")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Tab selection
        tab = st.radio("Select Mode", ["Analyze Stock", "View Models", "Model Comparison"])
    
    # Main content
    if tab == "Analyze Stock":
        analyze_stock_tab()
    elif tab == "View Models":
        view_models_tab()
    elif tab == "Model Comparison":
        model_comparison_tab()


def analyze_stock_tab():
    """Stock analysis tab"""
    
    st.header("Analyze Stock")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ticker = st.text_input("Stock Ticker", value="AAPL", help="e.g., AAPL, GOOGL, MSFT")
    
    with col2:
        interval = st.selectbox(
            "Interval",
            ["1d", "1h", "15m", "5m", "1m"],
            help="Candlestick interval"
        )
    
    with col3:
        days_back = st.number_input("Days Back", value=365, min_value=500, step=100)
    
    # Date range
    col1, col2 = st.columns(2)
    
    with col1:
        end_date = st.date_input("End Date", value=datetime.now())
    
    with col2:
        start_date = st.date_input("Start Date", value=end_date - timedelta(days=days_back))
    
    # Analyze button
    if st.button("🚀 Run Analysis", use_container_width=True):
        with st.spinner("Analyzing stock data..."):
            try:
                results = st.session_state.analyzer.analyze(
                    ticker,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                    interval=interval
                )
                
                st.session_state.results = results
                
                if results["status"] == "success":
                    st.success("✅ Analysis completed successfully!")
                    display_analysis_results(results)
                else:
                    st.error(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                logger.error(f"Analysis error: {str(e)}", exc_info=True)


def display_analysis_results(results):
    """Display analysis results"""
    
    st.markdown("---")
    st.header("📊 Analysis Results")
    
    # Metrics
    st.subheader("Model Performance Metrics")
    
    metrics = results["evaluation"]["metrics"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Accuracy", f"{metrics.get('accuracy', 0):.2%}")
    
    with col2:
        st.metric("Precision", f"{metrics.get('precision', 0):.2%}")
    
    with col3:
        st.metric("Recall", f"{metrics.get('recall', 0):.2%}")
    
    with col4:
        st.metric("F1-Score", f"{metrics.get('f1_score', 0):.4f}")
    
    # Top indicators
    st.subheader("🎯 Top Predictive Indicators")
    
    top_indicators = results["evaluation"]["report"]["top_3_indicators"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"🥇 {top_indicators[0]}")
    
    with col2:
        st.info(f"🥈 {top_indicators[1]}")
    
    with col3:
        st.info(f"🥉 {top_indicators[2]}")
    
    # Indicator rankings
    st.subheader("📈 Indicator Rankings")
    
    rankings = results["evaluation"]["report"]["indicator_rankings"]
    
    df_rankings = pd.DataFrame([
        {
            "Rank": r["rank"],
            "Indicator": r["indicator"],
            "Importance": f"{r['importance']:.4f}",
            "Correlation": f"{r['correlation']:.4f}"
        }
        for r in rankings
    ])
    
    st.dataframe(df_rankings, use_container_width=True)
    
    # Visualizations
    st.subheader("📊 Visualizations")
    
    viz_paths = results["evaluation"]["visualizations"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "feature_importance" in viz_paths:
            st.image(viz_paths["feature_importance"], caption="Feature Importance")
        
        if "confusion_matrix" in viz_paths:
            st.image(viz_paths["confusion_matrix"], caption="Confusion Matrix")
    
    with col2:
        if "roc_curve" in viz_paths:
            st.image(viz_paths["roc_curve"], caption="ROC Curve")
        
        if "indicator_correlation" in viz_paths:
            st.image(viz_paths["indicator_correlation"], caption="Indicator Correlation")
    
    # Insights and recommendations
    st.subheader("💡 Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Key Insights:**")
        for insight in results["evaluation"]["report"]["insights"]:
            st.write(f"• {insight}")
    
    with col2:
        st.markdown("**Recommendations:**")
        for rec in results["evaluation"]["report"]["recommendations"]:
            st.write(f"• {rec}")
    
    # Report text
    st.subheader("📄 Full Report")
    
    with st.expander("View Full Report"):
        st.text(results["evaluation"]["text_report"])


def view_models_tab():
    """View logged models tab"""
    
    st.header("📦 Logged Models")
    
    mlflow_registry = st.session_state.mlflow_registry
    
    # Get all models
    models = mlflow_registry.list_models()
    
    if not models:
        st.info("No models logged yet. Run an analysis to log models.")
        return
    
    # Display models
    df_models = pd.DataFrame([
        {
            "Run ID": m["run_id"][:8] + "...",
            "Stock": m["stock_ticker"],
            "Accuracy": f"{m['accuracy']:.2%}" if m['accuracy'] else "N/A",
            "Timestamp": m["timestamp"]
        }
        for m in models
    ])
    
    st.dataframe(df_models, use_container_width=True)
    
    # Filter by stock
    st.subheader("Filter by Stock")
    
    ticker = st.text_input("Stock Ticker", value="AAPL")
    
    if st.button("Search Models"):
        filtered_models = mlflow_registry.list_models(stock_ticker=ticker)
        
        if filtered_models:
            st.success(f"Found {len(filtered_models)} model(s) for {ticker}")
            
            df_filtered = pd.DataFrame([
                {
                    "Run ID": m["run_id"][:8] + "...",
                    "Accuracy": f"{m['accuracy']:.2%}" if m['accuracy'] else "N/A",
                    "Timestamp": m["timestamp"]
                }
                for m in filtered_models
            ])
            
            st.dataframe(df_filtered, use_container_width=True)
        else:
            st.warning(f"No models found for {ticker}")


def model_comparison_tab():
    """Model comparison tab"""
    
    st.header("🔄 Model Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ticker1 = st.text_input("Stock 1", value="AAPL")
    
    with col2:
        ticker2 = st.text_input("Stock 2", value="GOOGL")
    
    if st.button("Compare Models"):
        mlflow_registry = st.session_state.mlflow_registry
        
        run_id1, model1, metrics1 = mlflow_registry.get_best_model(ticker1)
        run_id2, model2, metrics2 = mlflow_registry.get_best_model(ticker2)
        
        if run_id1 and run_id2:
            # Create comparison dataframe
            comparison_data = {
                "Metric": ["Accuracy", "Precision", "Recall", "F1-Score"],
                ticker1: [
                    f"{metrics1.get('accuracy', 0):.2%}",
                    f"{metrics1.get('precision', 0):.2%}",
                    f"{metrics1.get('recall', 0):.2%}",
                    f"{metrics1.get('f1_score', 0):.4f}"
                ],
                ticker2: [
                    f"{metrics2.get('accuracy', 0):.2%}",
                    f"{metrics2.get('precision', 0):.2%}",
                    f"{metrics2.get('recall', 0):.2%}",
                    f"{metrics2.get('f1_score', 0):.4f}"
                ]
            }
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True)
            
            # Visualization
            fig = go.Figure(data=[
                go.Bar(name=ticker1, x=comparison_data["Metric"], 
                       y=[float(v.strip('%'))/100 for v in comparison_data[ticker1]]),
                go.Bar(name=ticker2, x=comparison_data["Metric"], 
                       y=[float(v.strip('%'))/100 for v in comparison_data[ticker2]])
            ])
            
            fig.update_layout(
                title="Model Performance Comparison",
                xaxis_title="Metric",
                yaxis_title="Score",
                barmode="group",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Could not find models for comparison")


if __name__ == "__main__":
    main()
