from typing import Dict, List
import pandas as pd

class StructureAnalyzer:

    def __init__(self, lookback_period: int = 20):
        self.lookback_period = lookback_period

    def find_support_resistance(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """Identify key support and resistance levels using swing highs/lows"""
        levels = {'support': [], 'resistance': []}

        for i in range(2, len(df) - 2):
            # Check for swing high
            if (
                df['High'].iloc[i] > df['High'].iloc[i-1] and 
                df['High'].iloc[i] > df['High'].iloc[i-2] and
                df['High'].iloc[i] > df['High'].iloc[i+1] and
                df['High'].iloc[i] > df['High'].iloc[i+2]
            ):
                levels['resistance'].append(df['High'].iloc[i])
            
            # Check for swing low
            if (
                df['Low'].iloc[i] < df['Low'].iloc[i-1] and 
                df['Low'].iloc[i] < df['Low'].iloc[i-2] and
                df['Low'].iloc[i] < df['Low'].iloc[i+1] and
                df['Low'].iloc[i] < df['Low'].iloc[i+2]
            ):
                levels['support'].append(df['Low'].iloc[i])

        return levels
    
    def is_break_of_structure(self, price: float, levels: Dict[str, List[float]], direction: str) -> bool:
        """Determine if current price breaks structure"""
        if direction == 'bullish':
            nearest_resistance = min((r for r in levels['resistance'] if r > price), default=None)
            return nearest_resistance is not None and price > nearest_resistance
        else:
            nearest_support = max((s for s in levels['support'] if s < price), default=None)
            return nearest_support is not None and price < nearest_support
