# enahaplots/themes.py
"""
Theme configuration for enahaplots visualization library.
Contains color palettes, fonts, and styling parameters for each theme.
"""

THEMES = {
    'cyberpunk': {
        'name': 'Cyberpunk',
        'background': '#0d0221',
        'figure_bg': '#1a0a2e',
        'primary': '#ff00ff',       # Neon magenta
        'secondary': '#00ffff',     # Cyan
        'accent': '#ffff00',        # Yellow
        'text': '#ffffff',
        'grid': '#3d1a5c',
        'colors': ['#ff00ff', '#00ffff', '#ffff00', '#ff6b6b', '#4ecdc4', '#95e1d3'],
        'font_family': 'monospace',
        'font_size': 12,
        'title_size': 16,
        'line_width': 2.5,
        'grid_alpha': 0.3,
        'grid_style': '--',
        'spine_width': 2,
        'marker_size': 80,
        'marker_edge_width': 2,
    },
    'nordic': {
        'name': 'Nordic',
        'background': '#2e3440',
        'figure_bg': '#3b4252',
        'primary': '#88c0d0',       # Frost blue
        'secondary': '#a3be8c',     # Aurora green
        'accent': '#ebcb8b',        # Aurora yellow
        'text': '#eceff4',
        'grid': '#4c566a',
        'colors': ['#88c0d0', '#a3be8c', '#ebcb8b', '#bf616a', '#b48ead', '#d08770'],
        'font_family': 'sans-serif',
        'font_size': 11,
        'title_size': 14,
        'line_width': 2.0,
        'grid_alpha': 0.25,
        'grid_style': '-',
        'spine_width': 1.5,
        'marker_size': 70,
        'marker_edge_width': 1.5,
    },
    'retro': {
        'name': 'Retro',
        'background': '#f5e6d3',
        'figure_bg': '#faf3eb',
        'primary': '#c44536',       # Burnt orange-red
        'secondary': '#772e25',     # Deep brown
        'accent': '#283d3b',        # Dark teal
        'text': '#2d2d2d',
        'grid': '#d4c4b0',
        'colors': ['#c44536', '#772e25', '#283d3b', '#d4a574', '#8b6914', '#4a5568'],
        'font_family': 'serif',
        'font_size': 11,
        'title_size': 15,
        'line_width': 2.2,
        'grid_alpha': 0.4,
        'grid_style': ':',
        'spine_width': 1.8,
        'marker_size': 75,
        'marker_edge_width': 1.8,
    }
}

# Default theme
DEFAULT_THEME = 'cyberpunk'


def get_theme(name: str = None) -> dict:
    """
    Get a theme configuration by name.
    
    Args:
        name: Theme name ('cyberpunk', 'nordic', or 'retro')
              If None, returns the default theme.
    
    Returns:
        Dictionary containing all theme configuration values.
    
    Raises:
        ValueError: If theme name is not found.
    """
    if name is None:
        name = DEFAULT_THEME
    
    name = name.lower()
    if name not in THEMES:
        available = ', '.join(THEMES.keys())
        raise ValueError(f"Theme '{name}' not found. Available themes: {available}")
    
    return THEMES[name]


def list_themes() -> list:
    """
    Get a list of all available theme names.
    
    Returns:
        List of theme name strings.
    """
    return list(THEMES.keys())


def get_color_cycle(theme_name: str = None) -> list:
    """
    Get the color cycle for a specific theme.
    
    Args:
        theme_name: Theme name. If None, uses default theme.
    
    Returns:
        List of color hex codes.
    """
    theme = get_theme(theme_name)
    return theme['colors']
