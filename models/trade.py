from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    entry_price: float
    stop_loss: float
    take_profit: float
    direction: float
    size: float
    symbol: str
    entry_time: datetime
    close_time: datetime
