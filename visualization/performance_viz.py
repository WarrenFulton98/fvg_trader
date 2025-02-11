# fvg_trading_bot/visualization/performance_viz.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class PerformanceVisualizer:
    def __init__(self, trades_df: pd.DataFrame, price_history: pd.DataFrame):
        """
        Initialize visualizer with trade data and price history
        
        trades_df columns: entry_time, exit_time, entry_price, exit_price, 
                         direction, size, pnl
        price_history columns: timestamp, Open, High, Low, Close, Volume
        """
        self.trades_df = trades_df
        self.price_history = price_history
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = [12, 7]
    
    def plot_equity_curve(self):
        """Plot cumulative P&L over time"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Calculate cumulative P&L
        cumulative_pnl = self.trades_df['pnl'].cumsum()
        
        # Calculate drawdown
        running_max = cumulative_pnl.cummax()
        drawdown = cumulative_pnl - running_max
        
        # Plot equity curve
        sns.lineplot(data=cumulative_pnl, ax=ax, color='blue', label='Equity Curve')
        
        # Plot drawdown
        ax2 = ax.twinx()
        sns.lineplot(data=drawdown, ax=ax2, color='red', alpha=0.3, label='Drawdown')
        
        # Formatting
        ax.set_title('Equity Curve and Drawdown')
        ax.set_xlabel('Trade Number')
        ax.set_ylabel('Cumulative P&L ($)')
        ax2.set_ylabel('Drawdown ($)')
        
        plt.tight_layout()
        return fig
    
    def plot_trade_distribution(self):
        """Plot distribution of trade P&Ls"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Histogram of P&L
        sns.histplot(data=self.trades_df, x='pnl', bins=30, ax=ax1)
        ax1.axvline(x=0, color='red', linestyle='--')
        ax1.set_title('Distribution of Trade P&L')
        ax1.set_xlabel('P&L ($)')
        
        # Box plot by trade direction
        sns.boxplot(data=self.trades_df, x='direction', y='pnl', ax=ax2)
        ax2.axhline(y=0, color='red', linestyle='--')
        ax2.set_title('P&L Distribution by Trade Direction')
        
        plt.tight_layout()
        return fig
    
    def plot_drawdown_analysis(self):
        """Detailed drawdown analysis"""
        cumulative_pnl = self.trades_df['pnl'].cumsum()
        running_max = cumulative_pnl.cummax()
        drawdown = (cumulative_pnl - running_max)
        drawdown_pct = drawdown / running_max * 100
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Drawdown over time
        sns.lineplot(data=drawdown, ax=ax1, color='red')
        ax1.set_title('Drawdown Over Time')
        ax1.set_ylabel('Drawdown ($)')
        
        # Drawdown distribution
        sns.histplot(data=drawdown_pct, bins=30, ax=ax2)
        ax2.set_title('Drawdown Distribution')
        ax2.set_xlabel('Drawdown (%)')
        
        plt.tight_layout()
        return fig
    
    def plot_time_analysis(self):
        """Analyze trading performance by time"""
        self.trades_df['hour'] = pd.to_datetime(self.trades_df['entry_time']).dt.hour
        self.trades_df['day_of_week'] = pd.to_datetime(self.trades_df['entry_time']).dt.day_name()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Average P&L by hour
        hourly_pnl = self.trades_df.groupby('hour')['pnl'].mean()
        sns.barplot(x=hourly_pnl.index, y=hourly_pnl.values, ax=ax1)
        ax1.set_title('Average P&L by Hour')
        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Average P&L ($)')
        
        # Average P&L by day of week
        daily_pnl = self.trades_df.groupby('day_of_week')['pnl'].mean()
        sns.barplot(x=daily_pnl.index, y=daily_pnl.values, ax=ax2)
        ax2.set_title('Average P&L by Day of Week')
        ax2.set_xlabel('Day of Week')
        ax2.set_ylabel('Average P&L ($)')
        
        plt.tight_layout()
        return fig
    
    def plot_price_with_trades(self):
        """Plot price chart with trade entries and exits"""
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Plot price
        sns.lineplot(data=self.price_history, x='timestamp', y='Close', ax=ax, label='Price')
        
        # Plot trade entries and exits
        for _, trade in self.trades_df.iterrows():
            # Entry point
            ax.scatter(trade['entry_time'], trade['entry_price'], 
                      color='green' if trade['direction'] == 'bullish' else 'red',
                      marker='^' if trade['direction'] == 'bullish' else 'v',
                      s=100)
            
            # Exit point
            ax.scatter(trade['exit_time'], trade['exit_price'],
                      color='blue', marker='s', s=100)
            
            # Connect entry and exit with a line
            ax.plot([trade['entry_time'], trade['exit_time']],
                   [trade['entry_price'], trade['exit_price']],
                   color='gray', linestyle='--', alpha=0.5)
        
        ax.set_title('Price Chart with Trades')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig
    
    def plot_performance_summary(self):
        """Create a comprehensive performance summary"""
        # Calculate metrics
        total_trades = len(self.trades_df)
        winning_trades = len(self.trades_df[self.trades_df['pnl'] > 0])
        losing_trades = len(self.trades_df[self.trades_df['pnl'] <= 0])
        win_rate = winning_trades / total_trades * 100
        
        avg_win = self.trades_df[self.trades_df['pnl'] > 0]['pnl'].mean()
        avg_loss = self.trades_df[self.trades_df['pnl'] <= 0]['pnl'].mean()
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        
        max_drawdown = (self.trades_df['pnl'].cumsum() - 
                       self.trades_df['pnl'].cumsum().cummax()).min()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')
        
        # Add text
        plt.text(0.1, 0.9, 'Performance Summary', fontsize=16, fontweight='bold')
        plt.text(0.1, 0.8, f'Total Trades: {total_trades}')
        plt.text(0.1, 0.7, f'Win Rate: {win_rate:.2f}%')
        plt.text(0.1, 0.6, f'Profit Factor: {profit_factor:.2f}')
        plt.text(0.1, 0.5, f'Average Win: ${avg_win:.2f}')
        plt.text(0.1, 0.4, f'Average Loss: ${avg_loss:.2f}')
        plt.text(0.1, 0.3, f'Max Drawdown: ${abs(max_drawdown):.2f}')
        
        plt.tight_layout()
        return fig
    
    def save_all_plots(self, output_dir: str):
        """Save all visualization plots to specified directory"""
        plots = {
            'equity_curve': self.plot_equity_curve(),
            'trade_distribution': self.plot_trade_distribution(),
            'drawdown_analysis': self.plot_drawdown_analysis(),
            'time_analysis': self.plot_time_analysis(),
            'price_with_trades': self.plot_price_with_trades(),
            'performance_summary': self.plot_performance_summary()
        }
        
        for name, fig in plots.items():
            fig.savefig(f'{output_dir}/{name}.png')
            plt.close(fig)

# Example usage:
"""
# After running backtest:
trades_df = pd.DataFrame(backtester.trades)
price_history = df  # Your price history DataFrame

visualizer = PerformanceVisualizer(trades_df, price_history)
visualizer.save_all_plots('trading_analysis')
"""