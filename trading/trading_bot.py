# fvg_trading_bot/trading/trading_bot.py
from typing import List, Dict
import asyncio
import yfinance as yf
import pandas as pd
from datetime import datetime
from models.trade import Trade
from models.fair_value_gap import FairValueGap
from analyzers.structure_analyzer import StructureAnalyzer
from analyzers.fvg_detector import FVGDetector
from utils.logger import get_logger

logger = get_logger(__name__)

class TradingBot:
    def __init__(self, symbols: List[str], min_gap_size: float = 0.01, 
                 volume_threshold: float = 1.5, risk_per_trade: float = 0.02):
        self.symbols = symbols
        self.fvg_detector = FVGDetector(min_gap_size, volume_threshold)
        self.structure_analyzer = StructureAnalyzer()
        self.risk_per_trade = risk_per_trade
        self.active_trades: Dict[str, Trade] = {}
        self.pending_fvgs: Dict[str, List[FairValueGap]] = {symbol: [] for symbol in symbols}

    async def fetch_data(self, symbol: str) -> pd.DataFrame:
        """Fetch historical data from yfinance"""
        ticker = yf.Ticker(symbol)
        df = ticker.history(period='1d', interval='5m')
        return df

    def calculate_position_size(self, entry_price: float, stop_loss: float, 
                              account_size: float) -> float:
        """Calculate position size based on risk parameters"""
        risk_amount = account_size * self.risk_per_trade
        risk_per_share = abs(entry_price - stop_loss)
        return risk_amount / risk_per_share

    async def monitor_symbol(self, symbol: str, account_size: float):
        """Monitor a single symbol for trading opportunities"""
        while True:
            try:
                df = await self.fetch_data(symbol)
                
                # Update structure levels
                levels = self.structure_analyzer.find_support_resistance(df)
                
                # Find new unmitigated FVGs
                unmitigated_fvgs = self.fvg_detector.find_fvg(df)  # This now returns only unmitigated FVGs
                self.pending_fvgs[symbol] = unmitigated_fvgs
                
                # Check for trade entries
                current_price = df['Close'].iloc[-1]
                
                for fvg in current_fvgs:
                    # Check if price is in FVG zone
                    if fvg.lower_price <= current_price <= fvg.upper_price:
                        # Verify break of structure
                        if self.structure_analyzer.is_break_of_structure(
                            current_price, levels, fvg.direction):
                            
                            # Calculate trade parameters
                            if fvg.direction == 'bullish':
                                entry_price = current_price
                                stop_loss = fvg.lower_price
                                take_profit = entry_price + (entry_price - stop_loss) * 2
                            else:
                                entry_price = current_price
                                stop_loss = fvg.upper_price
                                take_profit = entry_price - (stop_loss - entry_price) * 2
                            
                            # Calculate position size
                            size = self.calculate_position_size(
                                entry_price, stop_loss, account_size)
                            
                            # Create and execute trade
                            trade = Trade(
                                entry_price=entry_price,
                                stop_loss=stop_loss,
                                take_profit=take_profit,
                                direction=fvg.direction,
                                size=size,
                                symbol=symbol,
                                entry_time=datetime.now()
                            )
                            
                            self.active_trades[symbol] = trade
                            logger.info(f"Executed trade for {symbol}: {trade}")
                
                # Monitor active trades
                if symbol in self.active_trades:
                    trade = self.active_trades[symbol]
                    
                    # Check for stop loss or take profit
                    if (trade.direction == 'bullish' and 
                        (current_price <= trade.stop_loss or 
                         current_price >= trade.take_profit)):
                        logger.info(f"Closing trade for {symbol}")
                        del self.active_trades[symbol]
                    
                    elif (trade.direction == 'bearish' and 
                          (current_price >= trade.stop_loss or 
                           current_price <= trade.take_profit)):
                        logger.info(f"Closing trade for {symbol}")
                        del self.active_trades[symbol]
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error monitoring {symbol}: {str(e)}")
                await asyncio.sleep(60)

    async def run(self, account_size: float):
        """Run the trading bot across multiple symbols"""
        tasks = []
        for symbol in self.symbols:
            task = asyncio.create_task(self.monitor_symbol(symbol, account_size))
            tasks.append(task)
        
        await asyncio.gather(*tasks)
