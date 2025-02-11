# tests/conftest.py
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

@pytest.fixture
def sample_price_data():
    """Create sample price data for testing"""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='5min')
    data = {
        'Open': np.random.normal(100, 1, 100),
        'High': np.random.normal(101, 1, 100),
        'Low': np.random.normal(99, 1, 100),
        'Close': np.random.normal(100, 1, 100),
        'Volume': np.random.normal(1000000, 100000, 100)
    }
    df = pd.DataFrame(data, index=dates)
    # Ensure High is highest and Low is lowest
    df['High'] = df[['Open', 'High', 'Close']].max(axis=1) + 0.1
    df['Low'] = df[['Open', 'Low', 'Close']].min(axis=1) - 0.1
    return df

@pytest.fixture
def sample_fvg_data():
    """Create sample data with known FVGs"""
    dates = pd.date_range(start='2024-01-01', periods=5, freq='5min')
    data = {
        'Open':  [100, 100, 100, 104, 104],
        'High':  [101, 101, 101, 105, 105],
        'Low':   [99,  99,  99,  103, 103],
        'Close': [100, 100, 100, 104, 104],
        'Volume': [1000000] * 5
    }
    return pd.DataFrame(data, index=dates)

# tests/test_models.py
from fvg_trading_bot.models.fair_value_gap import FairValueGap
from fvg_trading_bot.models.trade import Trade
from datetime import datetime

def test_fair_value_gap_creation():
    fvg = FairValueGap(
        start_time=datetime(2024, 1, 1),
        end_time=datetime(2024, 1, 1, 0, 5),
        upper_price=105.0,
        lower_price=100.0,
        volume_weight=1.5,
        direction='bullish'
    )
    assert fvg.direction == 'bullish'
    assert fvg.mitigated == False
    assert fvg.upper_price == 105.0
    assert fvg.lower_price == 100.0

def test_fair_value_gap_price_checks():
    fvg = FairValueGap(
        start_time=datetime(2024, 1, 1),
        end_time=datetime(2024, 1, 1, 0, 5),
        upper_price=105.0,
        lower_price=100.0,
        volume_weight=1.5,
        direction='bullish'
    )
    assert fvg.is_price_in_gap(102.5) == True
    assert fvg.is_price_in_gap(99.0) == False
    assert fvg.is_price_in_gap(106.0) == False

def test_trade_creation():
    trade = Trade(
        entry_price=100.0,
        stop_loss=98.0,
        take_profit=104.0,
        direction='bullish',
        size=100,
        symbol='AAPL',
        entry_time=datetime(2024, 1, 1)
    )
    assert trade.direction == 'bullish'
    assert trade.size == 100
    assert trade.symbol == 'AAPL'

# tests/test_analyzers.py
from fvg_trading_bot.analyzers.structure_analyzer import StructureAnalyzer
from fvg_trading_bot.analyzers.fvg_detector import FVGDetector

def test_structure_analyzer(sample_price_data):
    analyzer = StructureAnalyzer(lookback_period=10)
    levels = analyzer.find_support_resistance(sample_price_data)
    
    assert 'support' in levels
    assert 'resistance' in levels
    assert isinstance(levels['support'], list)
    assert isinstance(levels['resistance'], list)

def test_break_of_structure(sample_price_data):
    analyzer = StructureAnalyzer(lookback_period=10)
    levels = analyzer.find_support_resistance(sample_price_data)
    
    # Test bullish break
    if levels['resistance']:
        price = max(levels['resistance']) + 0.1
        assert analyzer.is_break_of_structure(price, levels, 'bullish') == True
    
    # Test bearish break
    if levels['support']:
        price = min(levels['support']) - 0.1
        assert analyzer.is_break_of_structure(price, levels, 'bearish') == True

def test_fvg_detector(sample_fvg_data):
    detector = FVGDetector(min_gap_size=0.5, volume_threshold=0.5)
    fvgs = detector.find_fvg(sample_fvg_data)
    
    assert len(fvgs) > 0
    for fvg in fvgs:
        assert isinstance(fvg.upper_price, float)
        assert isinstance(fvg.lower_price, float)
        assert fvg.direction in ['bullish', 'bearish']
        assert fvg.volume_weight >= 0.5

# tests/test_trading.py
import pytest
from fvg_trading_bot.trading.trading_bot import TradingBot

@pytest.mark.asyncio
async def test_trading_bot_initialization():
    bot = TradingBot(
        symbols=['AAPL'],
        min_gap_size=0.5,
        volume_threshold=1.5,
        risk_per_trade=0.02
    )
    assert bot.symbols == ['AAPL']
    assert bot.risk_per_trade == 0.02

@pytest.mark.asyncio
async def test_position_size_calculation():
    bot = TradingBot(
        symbols=['AAPL'],
        min_gap_size=0.5,
        volume_threshold=1.5,
        risk_per_trade=0.02
    )
    
    position_size = bot.calculate_position_size(
        entry_price=100.0,
        stop_loss=98.0,
        account_size=100000.0
    )
    
    expected_size = (100000.0 * 0.02) / 2.0  # 2.0 is the risk per share
    assert abs(position_size - expected_size) < 0.01

# tests/test_backtesting.py
from fvg_trading_bot.backtesting.backtester import Backtester
from fvg_trading_bot.trading.trading_bot import TradingBot

def test_backtester_initialization(sample_price_data):
    bot = TradingBot(
        symbols=['AAPL'],
        min_gap_size=0.5,
        volume_threshold=1.5,
        risk_per_trade=0.02
    )
    backtester = Backtester(bot)
    assert backtester.trading_bot == bot
    assert len(backtester.trades) == 0

def test_backtest_results(sample_price_data):
    bot = TradingBot(
        symbols=['AAPL'],
        min_gap_size=0.5,
        volume_threshold=1.5,
        risk_per_trade=0.02
    )
    backtester = Backtester(bot)
    
    results = backtester.run(
        symbol='AAPL',
        start_date='2024-01-01',
        end_date='2024-01-02',
        initial_capital=100000
    )
    
    assert isinstance(results, pd.DataFrame)
    if len(results) > 0:
        assert 'entry_price' in results.columns
        assert 'exit_price' in results.columns
        assert 'pnl' in results.columns

# tests/test_visualization.py
from fvg_trading_bot.visualization.performance_viz import PerformanceVisualizer
import matplotlib.pyplot as plt

def test_visualizer_initialization(sample_price_data, tmp_path):
    trades_df = pd.DataFrame({
        'entry_time': pd.date_range(start='2024-01-01', periods=5),
        'exit_time': pd.date_range(start='2024-01-01', periods=5) + pd.Timedelta(hours=1),
        'entry_price': [100, 101, 102, 103, 104],
        'exit_price': [101, 102, 103, 104, 105],
        'direction': ['bullish'] * 5,
        'size': [100] * 5,
        'pnl': [100] * 5
    })
    
    visualizer = PerformanceVisualizer(trades_df, sample_price_data)
    
    # Test plot generation
    fig = visualizer.plot_equity_curve()
    assert isinstance(fig, plt.Figure)
    plt.close(fig)
    
    # Test save functionality
    output_dir = tmp_path / "test_output"
    output_dir.mkdir()
    visualizer.save_all_plots(str(output_dir))
    assert (output_dir / "equity_curve.png").exists()
