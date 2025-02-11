from ..visualization.performance_viz import PerformanceVisualizer
import matplotlib.pyplot as plt
import pandas as pd

def test_visualizer_initialization(sample_price_data, tmp_path):
    trades_df = pd.DataFrame({
        'entry_time': pd.date_range(start='2024-01-01', periods=5),
        'exit_time': pd.date_range(start='2024-01-01', periods=5) + pd.Timedelta(hours=1),
        'entry_price': [100, 101, 102, 103, 104],
        'exit_price': [101, 102, 103, 104, 105],
        'direction': ['bullish'] * 5,
        'size': [100] * 5,
        'pnl': [100] * 5
    })
    
    visualizer = PerformanceVisualizer(trades_df, sample_price_data)
    
    # Test plot generation
    fig = visualizer.plot_equity_curve()
    assert isinstance(fig, plt.Figure)
    plt.close(fig)
    
    # Test save functionality
    output_dir = tmp_path / "test_output"
    output_dir.mkdir()
    visualizer.save_all_plots(str(output_dir))
    assert (output_dir / "equity_curve.png").exists()
