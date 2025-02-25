from typing import List
import pandas as pd
from models.fair_value_gap import FairValueGap

class FVGDetector:
    def __init__(self, min_gap_size: float, volume_threshold: float):
        self.min_gap_size = min_gap_size
        self.volume_threshold = volume_threshold
        self.active_fvgs: List[FairValueGap] = []  # Track active FVGs

    def update_fvg_status(self, price: float) -> None:
        """Update mitigation status of all tracked FVGs"""
        for fvg in self.active_fvgs:
            if not fvg.mitigated and fvg.is_mitigated_by_price(price):
                fvg.mitigated = True

    def find_fvg(self, df: pd.DataFrame) -> List[FairValueGap]:
        """Detect Fair Value Gaps in the price action"""
        # Update existing FVGs status
        current_price = df['Close'].iloc[-1]
        self.update_fvg_status(current_price)
        
        # Find new FVGs
        new_fvgs = []
        
        for i in range(1, len(df) - 1):
            # Bullish FVG
            if df['Low'].iloc[i+1] > df['High'].iloc[i-1]:
                gap_size = df['Low'].iloc[i+1] - df['High'].iloc[i-1]
                if gap_size >= self.min_gap_size:
                    volume_weight = df['Volume'].iloc[i] / df['Volume'].mean()
                    if volume_weight >= self.volume_threshold:
                        fvg = FairValueGap(
                            start_time=df.index[i-1],
                            end_time=df.index[i+1],
                            upper_price=df['Low'].iloc[i+1],
                            lower_price=df['High'].iloc[i-1],
                            volume_weight=volume_weight,
                            direction='bullish',
                            mitigated=False
                        )
                        # Check if already mitigated by current price
                        if fvg.is_mitigated_by_price(current_price):
                            fvg.mitigated = True
                        new_fvgs.append(fvg)
            
            # Bearish FVG
            if df['High'].iloc[i+1] < df['Low'].iloc[i-1]:
                gap_size = df['Low'].iloc[i-1] - df['High'].iloc[i+1]
                if gap_size >= self.min_gap_size:
                    volume_weight = df['Volume'].iloc[i] / df['Volume'].mean()
                    if volume_weight >= self.volume_threshold:
                        fvg = FairValueGap(
                            start_time=df.index[i-1],
                            end_time=df.index[i+1],
                            upper_price=df['Low'].iloc[i-1],
                            lower_price=df['High'].iloc[i+1],
                            volume_weight=volume_weight,
                            direction='bearish',
                            mitigated=False
                        )
                        # Check if already mitigated by current price
                        if fvg.is_mitigated_by_price(current_price):
                            fvg.mitigated = True
                        new_fvgs.append(fvg)
        
        # Update active FVGs list with new ones
        self.active_fvgs.extend(new_fvgs)
        
        # Remove mitigated FVGs older than the lookback period
        cutoff_time = df.index[-1] - pd.Timedelta(days=7)  # Keep 7 days of history
        self.active_fvgs = [
            fvg for fvg in self.active_fvgs 
            if not (fvg.mitigated and fvg.end_time < cutoff_time)
        ]
        
        return [fvg for fvg in self.active_fvgs if not fvg.mitigated]  # Return only unmitigated FVGs
