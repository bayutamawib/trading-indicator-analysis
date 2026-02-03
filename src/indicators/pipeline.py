"""Indicator calculation pipeline"""

import pandas as pd
from .atr import ATRCalculator
from .sma import SMACalculator
from .bollinger_bands import BollingerBandsCalculator
from .rsi import RSICalculator
from .macd import MACDCalculator
from .stochastic import StochasticCalculator
from .adx import ADXCalculator
from .cci import CCICalculator


class IndicatorPipeline:
    """Orchestrates calculation of all technical indicators"""
    
    def __init__(self):
        """Initialize indicator pipeline with all calculators"""
        self.calculators = [
            ATRCalculator(period=14),
            SMACalculator(periods=[20, 50]),
            BollingerBandsCalculator(period=20, std_dev=2.0),
            RSICalculator(period=14),
            MACDCalculator(fast_period=12, slow_period=26, signal_period=9),
            StochasticCalculator(period=14, smoothing=3),
            ADXCalculator(period=14),
            CCICalculator(period=20),
        ]
    
    def calculate_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all indicators for given OHLCV data
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with original OHLCV data plus all calculated indicators
        """
        result = df.copy()
        
        for calculator in self.calculators:
            result = calculator.calculate(result)
        
        return result
    
    def get_indicator_columns(self) -> list:
        """Get list of all indicator column names
        
        Returns:
            List of indicator column names
        """
        indicators = [
            "ATR",
            "SMA_20", "SMA_50",
            "BB_Upper", "BB_Middle", "BB_Lower",
            "RSI",
            "MACD", "MACD_Signal", "MACD_Histogram",
            "Stoch_K", "Stoch_D",
            "ADX",
            "CCI"
        ]
        return indicators
