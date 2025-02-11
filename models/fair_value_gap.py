from dataclasses import dataclass
from datetime import datetime

@dataclass
class FairValueGap:
    start_time: datetime
    end_time: datetime
    upper_price: float
    lower_price: float
    volume_weight: float
    direction: str # 'bullish' or 'bearish'
    mitigated: bool = False # Track if the FVG has been filled

    def is_price_in_gap(self, price: float) -> bool:
        """Check if a price is within the FVG range"""
        return self.lower_price <= price <= self.upper_price
    
    def is_mitigated_by_price(self, price: float) -> bool:
        """Check if price action mitigates this FVG"""
        if self.direction == 'bullish':
            return price <= self.lower_price
        else:
            return price >= self.upper_price
