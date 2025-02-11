from ..models.fair_value_gap import FairValueGap
from ..models.trade import Trade
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
