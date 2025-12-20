# enahaplots/__init__.py
"""
enahaplots - A Personal Python Visualization Library

A stylish, themed visualization library built on matplotlib with
built-in statistical analysis features including outlier detection
and forecasting.

Usage:
    import enahaplots
    
    enahaplots.styled_line(
        x=[1, 2, 3, 4, 5],
        y=[10, 20, 15, 25, 30],
        title="My Styled Plot",
        style="cyberpunk"
    )

Available themes: 'cyberpunk', 'nordic', 'retro'
"""

__version__ = "1.0.0"
__author__ = "Enaha"

# Import all plotting functions
from .plots import (
    styled_line,
    styled_bar,
    styled_scatter,
    styled_pie,
    styled_histogram,
    styled_heatmap,
)

# Import theme utilities
from .themes import (
    get_theme,
    list_themes,
    get_color_cycle,
    THEMES,
    DEFAULT_THEME,
)

# Import math utilities
from .math_engine import (
    detect_outliers,
    forecast,
    calculate_trend,
    calculate_statistics,
    moving_average,
    normalize,
)

# Define public API
__all__ = [
    # Plotting functions
    'styled_line',
    'styled_bar',
    'styled_scatter',
    'styled_pie',
    'styled_histogram',
    'styled_heatmap',
    # Theme utilities
    'get_theme',
    'list_themes',
    'get_color_cycle',
    'THEMES',
    'DEFAULT_THEME',
    # Math utilities
    'detect_outliers',
    'forecast',
    'calculate_trend',
    'calculate_statistics',
    'moving_average',
    'normalize',
]
