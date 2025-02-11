import pytest
from ..trading.trading_bot import TradingBot

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
