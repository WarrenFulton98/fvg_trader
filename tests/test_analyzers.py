from ..analyzers.structure_analyzer import StructureAnalyzer
from ..analyzers.fvg_detector import FVGDetector

def test_structure_analyzer(sample_price_data):
    analyzer = StructureAnalyzer(lookback_period=10)
    levels = analyzer.find_support_resistance(sample_price_data)
    
    assert 'support' in levels
    assert 'resistance' in levels
    assert isinstance(levels['support'], list)
    assert isinstance(levels['resistance'], list)

def test_break_of_structure(sample_price_data):
    analyzer = StructureAnalyzer(lookback_period=10)
    levels = analyzer.find_support_resistance(sample_price_data)
    
    # Test bullish break
    if levels['resistance']:
        price = max(levels['resistance']) + 0.1
        assert analyzer.is_break_of_structure(price, levels, 'bullish') == True
    
    # Test bearish break
    if levels['support']:
        price = min(levels['support']) - 0.1
        assert analyzer.is_break_of_structure(price, levels, 'bearish') == True

def test_fvg_detector(sample_fvg_data):
    detector = FVGDetector(min_gap_size=0.5, volume_threshold=0.5)
    fvgs = detector.find_fvg(sample_fvg_data)
    
    assert len(fvgs) > 0
    for fvg in fvgs:
        assert isinstance(fvg.upper_price, float)
        assert isinstance(fvg.lower_price, float)
        assert fvg.direction in ['bullish', 'bearish']
        assert fvg.volume_weight >= 0.5