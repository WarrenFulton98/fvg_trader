from ..backtesting.backtester import Backtester
from ..trading.trading_bot import TradingBot
import pandas as pd

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
