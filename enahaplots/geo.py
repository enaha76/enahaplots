# enahaplots/geo.py

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import contextily as ctx
from .themes import get_theme, DEFAULT_THEME
from .plots import _apply_theme

def styled_map(
    gdf: gpd.GeoDataFrame,
    column: str,
    title: str = "",
    style: str = DEFAULT_THEME,
    cmap: str = None,
    add_basemap: bool = True,
    figsize: tuple = (12, 8),
    save_path: str = None,
    show: bool = True
) -> plt.Figure:
    """
    Create a professional styled choropleth map.
    """
    # 1. TECHNICAL FIX: Data Sanitization (Timestamp cleaning)
    # Detects datetime64 columns (like 'date' and 'validOn') and converts to string
    for col in gdf.columns:
        if pd.api.types.is_datetime64_any_dtype(gdf[col]):
            gdf[col] = gdf[col].dt.strftime('%Y-%m-%d')

    # 2. Theme Initialization
    theme = get_theme(style)
    fig, ax = plt.subplots(figsize=figsize)
    
    # 3. GIS AMELIORATION: CRS Management
    # Ensure data is in Web Mercator for basemap compatibility
    if gdf.crs != "EPSG:3857":
        gdf = gdf.to_crs(epsg=3857)

    # 4. Thematic Rendering
    if cmap is None:
        cmap = 'plasma' if style == 'cyberpunk' else 'YlGnBu'

    gdf.plot(
        column=column,
        ax=ax,
        cmap=cmap,
        legend=True,
        edgecolor=theme['grid'],
        linewidth=0.5,
        alpha=0.8,
        legend_kwds={'label': column, 'orientation': "vertical", 'shrink': 0.7}
    )

    # 5. Adding Interactive Tiles (Basemap)
    if add_basemap:
        source = ctx.providers.CartoDB.Positron if style != 'cyberpunk' else ctx.providers.CartoDB.DarkMatter
        ctx.add_basemap(ax, source=source)

    # 6. Apply enahaplots Theme Logic
    _apply_theme(ax, fig, theme, title)
    ax.set_axis_off()  # Standard GIS storytelling: hide coordinate axes

    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, facecolor=theme['figure_bg'])
    
    if show:
        plt.show()
        
    return fig
