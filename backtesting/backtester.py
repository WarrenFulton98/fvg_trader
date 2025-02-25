# fvg_trading_bot/backtesting/backtester.py
from typing import List, Dict
import pandas as pd
import yfinance as yf
from trading.trading_bot import TradingBot
from utils.logger import get_logger
from visualization.performance_viz import PerformanceVisualizer

logger = get_logger(__name__)

class Backtester:
    def __init__(self, trading_bot: TradingBot):
        self.trading_bot = trading_bot
        self.trades: List[Dict] = []
        
    def run(self, symbol: str, start_date: str, end_date: str, 
            initial_capital: float) -> pd.DataFrame:
        """Run backtest for a single symbol"""
        # Fetch historical data
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date, interval='5m')
        
        capital = initial_capital
        current_trade = None
        
        for i in range(len(df)):
            current_price = df['Close'].iloc[i]
            
            # Find FVGs
            if i >= 3:
                test_df = df.iloc[max(0, i-20):i+1]
                fvgs = self.trading_bot.fvg_detector.find_fvg(test_df)
                levels = self.trading_bot.structure_analyzer.find_support_resistance(test_df)
                
                # Check for trade entry
                if not current_trade:
                    for fvg in fvgs:
                        if (fvg.lower_price <= current_price <= fvg.upper_price and
                            self.trading_bot.structure_analyzer.is_break_of_structure(
                                current_price, levels, fvg.direction)):
                            
                            # Calculate trade parameters
                            if fvg.direction == 'bullish':
                                entry_price = current_price
                                stop_loss = fvg.lower_price
                                take_profit = entry_price + (entry_price - stop_loss) * 2
                            else:
                                entry_price = current_price
                                stop_loss = fvg.upper_price
                                take_profit = entry_price - (stop_loss - entry_price) * 2
                            
                            size = self.trading_bot.calculate_position_size(
                                entry_price, stop_loss, capital)
                            
                            current_trade = {
                                'entry_price': entry_price,
                                'stop_loss': stop_loss,
                                'take_profit': take_profit,
                                'direction': fvg.direction,
                                'size': size,
                                'entry_time': df.index[i],
                                'volume_weight': fvg.volume_weight
                            }
                
                # Check for trade exit
                elif current_trade:
                    if current_trade['direction'] == 'bullish':
                        if (current_price <= current_trade['stop_loss'] or 
                            current_price >= current_trade['take_profit']):
                            
                            pnl = (current_price - current_trade['entry_price']) * current_trade['size']
                            capital += pnl
                            
                            self.trades.append({
                                **current_trade,
                                'exit_price': current_price,
                                'exit_time': df.index[i],
                                'pnl': pnl
                            })
                            
                            current_trade = None
                    
                    else:  # bearish
                        if (current_price >= current_trade['stop_loss'] or 
                            current_price <= current_trade['take_profit']):
                            
                            pnl = (current_trade['entry_price'] - current_price) * current_trade['size']
                            capital += pnl
                            
                            self.trades.append({
                                **current_trade,
                                'exit_price': current_price,
                                'exit_time': df.index[i],
                                'pnl': pnl
                            })
                            
                            current_trade = None
        
        trades_df = pd.DataFrame(self.trades)
        
        # Create visualizations
        visualizer = PerformanceVisualizer(trades_df, df)
        #visualizer.save_all_plots('trading_analysis')
        
        return trades_df

    def get_performance_metrics(self) -> Dict:
        """Calculate and return performance metrics from backtest results"""
        df = pd.DataFrame(self.trades)
        if len(df) == 0:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'average_win': 0,
                'average_loss': 0,
                'largest_win': 0,
                'largest_loss': 0,
                'total_pnl': 0
            }

        winning_trades = df[df['pnl'] > 0]
        losing_trades = df[df['pnl'] < 0]

        return {
            'total_trades': len(df),
            'win_rate': len(winning_trades) / len(df) if len(df) > 0 else 0,
            'profit_factor': abs(winning_trades['pnl'].sum() / losing_trades['pnl'].sum()) if len(losing_trades) > 0 else float('inf'),
            'average_win': winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0,
            'average_loss': abs(losing_trades['pnl'].mean()) if len(losing_trades) > 0 else 0,
            'largest_win': winning_trades['pnl'].max() if len(winning_trades) > 0 else 0,
            'largest_loss': abs(losing_trades['pnl'].min()) if len(losing_trades) > 0 else 0,
            'total_pnl': df['pnl'].sum()
        }
