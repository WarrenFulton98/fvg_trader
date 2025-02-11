# FVG Trading Bot

A Python-based trading bot that implements a Fair Value Gap (FVG) strategy with break of structure confirmation. The bot can simultaneously monitor multiple symbols, perform backtesting, and provide detailed performance visualization.

## Features

### Trading Strategy
- Fair Value Gap (FVG) detection with volume weighting
- Break of structure confirmation
- Support and resistance level analysis
- Multi-symbol monitoring
- Risk management based on position sizing

### Technical Features
- Asynchronous real-time trading
- Comprehensive backtesting framework
- Detailed performance visualization
- Historical data retrieval using yfinance
- Clean, modular architecture

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Option 1: Installing from Source
```bash
# Clone the repository
git clone https://github.com/yourusername/fvg_trading_bot.git
cd fvg_trading_bot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Usage

## Testing

### Setting Up Test Environment

1. Install test dependencies:
```bash
# If you installed with pip
pip install "fvg_trading_bot[dev]"

# Or if you're developing locally
pip install -e ".[dev]"
```

2. Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=fvg_trading_bot

# Run specific test file
pytest tests/test_models.py
```

### Test Structure

The test suite covers:

1. Models (`test_models.py`)
   - FairValueGap creation and validation
   - Trade object creation and properties

2. Analyzers (`test_analyzers.py`)
   - Structure analysis
   - Support/resistance detection
   - FVG detection

3. Trading Logic (`test_trading.py`)
   - Bot initialization
   - Position sizing
   - Trade execution

4. Backtesting (`test_backtesting.py`)
   - Backtester initialization
   - Results validation
   - Performance metrics

5. Visualization (`test_visualization.py`)
   - Chart generation
   - Performance metrics visualization

### Adding New Tests

When adding new features, please ensure:
1. Test coverage for new functionality
2. Integration tests if needed
3. proper use of pytest fixtures
4. Async tests for trading functions

Example

### Quick Start
```python
from fvg_trader.trading.trading_bot import TradingBot
from fvg_trader.backtesting.backtester import Backtester

# Initialize the trading bot
symbols = ['AAPL', 'MSFT', 'GOOGL']
bot = TradingBot(
    symbols=symbols,
    min_gap_size=0.5,  # Minimum gap size in dollars
    volume_threshold=1.5,  # Minimum volume ratio
    risk_per_trade=0.02  # 2% risk per trade
)

# Run backtest
backtester = Backtester(bot)
results = backtester.run(
    symbol='AAPL',
    start_date='2024-01-01',
    end_date='2024-02-01',
    initial_capital=100000
)

# View performance metrics
print(results)
```

### Live Trading
```python
import asyncio

# Run live trading with $100,000 initial capital
asyncio.run(bot.run(100000))
```

## Trading Strategy Details

### Fair Value Gap (FVG)
A Fair Value Gap occurs when there is a significant gap between candles that represents an imbalance in the market. The bot identifies these gaps and weights them by volume to determine significance.

Requirements for a valid FVG trade:
1. Gap size must be larger than specified threshold
2. Must coincide with a break of structure
3. Price must return to the FVG zone
4. Stop loss is placed at the opposite end of the FVG

### Position Sizing
The bot uses a risk-based position sizing approach:
- Each trade risks a specified percentage of account equity
- Position size is calculated based on the distance to stop loss
- Volume is considered in the entry decision

## Performance Visualization

The bot includes comprehensive visualization tools that show:
1. Equity Curve with Drawdown
2. Trade Distribution Analysis
3. Drawdown Analysis
4. Time-based Performance Analysis
5. Price Chart with Trade Entries/Exits
6. Performance Summary Statistics

Example of generating visualizations:
```python
from fvg_trading_bot.visualization.performance_viz import PerformanceVisualizer

visualizer = PerformanceVisualizer(trades_df, price_history_df)
visualizer.save_all_plots('trading_analysis')
```

## Project Structure
```
fvg_trading_bot/
│
├── fvg_trading_bot/
│   ├── models/
│   │   ├── fair_value_gap.py
│   │   └── trade.py
│   │
│   ├── analyzers/
│   │   ├── structure_analyzer.py
│   │   └── fvg_detector.py
│   │
│   ├── trading/
│   │   └── trading_bot.py
│   │
│   ├── backtesting/
│   │   └── backtester.py
│   │
│   ├── visualization/
│   │   └── performance_viz.py
│   │
│   └── utils/
│       └── logger.py
│
└── examples/
    └── main.py
```

## Configuration

Key parameters that can be configured:
- `min_gap_size`: Minimum size for a valid FVG
- `volume_threshold`: Minimum volume ratio for FVG validation
- `risk_per_trade`: Percentage of account to risk per trade
- `lookback_period`: Period for structure analysis

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is for educational purposes only. Use at your own risk. The authors and contributors are not responsible for any financial losses incurred through the use of this trading bot.