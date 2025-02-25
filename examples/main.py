import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trading.trading_bot import TradingBot
from backtesting.backtester import Backtester
from utils.logger import get_logger

logger = get_logger(__name__)

async def main():
    # Configuration
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    initial_capital = 100000
    min_gap_size = 0.5
    volume_threshold = 1.5
    risk_per_trade = 0.02

    # Create trading bot instance
    bot = TradingBot(
        symbols=symbols,
        min_gap_size=min_gap_size,
        volume_threshold=volume_threshold,
        risk_per_trade=risk_per_trade
    )

    # Run backtest first
    logger.info("Starting backtest...")
    backtester = Backtester(bot)
    
    for symbol in symbols:
        logger.info(f"Backtesting {symbol}...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        results = backtester.run(
            symbol=symbol,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            initial_capital=initial_capital
        )
        
        metrics = backtester.get_performance_metrics()
        
        logger.info(f"\nBacktest Results for {symbol}:")
        logger.info(f"Total Trades: {metrics['total_trades']}")
        logger.info(f"Win Rate: {metrics['win_rate']*100:.2f}%")
        logger.info(f"Profit Factor: {metrics['profit_factor']:.2f}")
        logger.info(f"Average Win: ${metrics['average_win']:.2f}")
        logger.info(f"Average Loss: ${metrics['average_loss']:.2f}")
        logger.info(f"Largest Win: ${metrics['largest_win']:.2f}")
        logger.info(f"Largest Loss: ${metrics['largest_loss']:.2f}")
        logger.info(f"Total PnL: ${metrics['total_pnl']:.2f}\n")

    # Start live trading
    logger.info("Starting live trading...")
    await bot.run(initial_capital)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down trading bot...")
        sys.exit(0)
