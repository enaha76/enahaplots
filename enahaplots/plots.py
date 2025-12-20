# enahaplots/plots.py
"""
Main plotting functions for enahaplots.
Provides styled visualization functions with consistent theming.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import List, Optional, Union, Tuple
from .themes import get_theme, DEFAULT_THEME
from .math_engine import detect_outliers, forecast as calc_forecast, calculate_trend


def _apply_theme(ax, fig, theme: dict, title: str = None):
    """Apply theme styling to axes and figure."""
    # Figure background
    fig.patch.set_facecolor(theme['figure_bg'])
    ax.set_facecolor(theme['background'])
    
    # Grid
    ax.grid(True, alpha=theme['grid_alpha'], color=theme['grid'], 
            linestyle=theme['grid_style'], linewidth=0.8)
    
    # Spines
    for spine in ax.spines.values():
        spine.set_color(theme['grid'])
        spine.set_linewidth(theme['spine_width'])
    
    # Tick colors
    ax.tick_params(colors=theme['text'], labelsize=theme['font_size'])
    
    # Labels color
    ax.xaxis.label.set_color(theme['text'])
    ax.yaxis.label.set_color(theme['text'])
    
    # Title
    if title:
        ax.set_title(title, fontsize=theme['title_size'], 
                     fontweight='bold', color=theme['text'],
                     fontfamily=theme['font_family'], pad=15)


def _create_figure(theme: dict, figsize: Tuple[int, int] = (10, 6)):
    """Create a new figure with theme styling."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(theme['figure_bg'])
    return fig, ax


def styled_line(
    x: List = None,
    y: List = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    style: str = DEFAULT_THEME,
    show_outliers: bool = False,
    show_forecast: bool = False,
    forecast_periods: int = 5,
    show_trend: bool = False,
    line_label: str = None,
    figsize: Tuple[int, int] = (10, 6),
    save_path: str = None,
    show: bool = True
) -> plt.Figure:
    """
    Create a styled line chart.
    
    Args:
        x: X-axis values. If None, uses indices.
        y: Y-axis values (required).
        title: Chart title.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        style: Theme name ('cyberpunk', 'nordic', 'retro').
        show_outliers: Highlight outlier points.
        show_forecast: Show predicted future values.
        forecast_periods: Number of periods to forecast.
        show_trend: Show trend line.
        line_label: Label for legend.
        figsize: Figure size as (width, height).
        save_path: Path to save the figure.
        show: Whether to display the plot.
    
    Returns:
        matplotlib Figure object.
    """
    if y is None:
        raise ValueError("y values are required")
    
    y = list(y)
    if x is None:
        x = list(range(len(y)))
    else:
        x = list(x)
    
    theme = get_theme(style)
    fig, ax = _create_figure(theme, figsize)
    
    # Main line
    ax.plot(x, y, color=theme['primary'], linewidth=theme['line_width'],
            marker='o', markersize=6, markerfacecolor=theme['secondary'],
            markeredgecolor=theme['primary'], markeredgewidth=1.5,
            label=line_label or 'Data', zorder=3)
    
    # Outliers
    if show_outliers:
        indices, values = detect_outliers(y)
        if indices:
            outlier_x = [x[i] for i in indices]
            ax.scatter(outlier_x, values, s=theme['marker_size'] * 2,
                      facecolors='none', edgecolors=theme['accent'],
                      linewidths=3, zorder=5, label='Outliers')
            for ox, ov in zip(outlier_x, values):
                ax.annotate(f'⚠ {ov:.1f}', (ox, ov), 
                           textcoords="offset points", xytext=(10, 10),
                           fontsize=9, color=theme['accent'],
                           fontweight='bold')
    
    # Trend line
    if show_trend:
        slope, intercept, direction = calculate_trend(x, y)
        trend_y = [slope * xi + intercept for xi in x]
        ax.plot(x, trend_y, color=theme['secondary'], linewidth=1.5,
                linestyle='--', alpha=0.7, label=f'Trend ({direction})')
    
    # Forecast
    if show_forecast:
        fx, fy = calc_forecast(x, y, forecast_periods)
        ax.plot(fx, fy, color=theme['accent'], linewidth=theme['line_width'],
                linestyle='--', marker='s', markersize=5,
                label=f'Forecast ({forecast_periods} periods)', zorder=2)
        # Shade forecast region
        ax.axvspan(x[-1], fx[-1], alpha=0.1, color=theme['accent'])
    
    # Apply theme
    _apply_theme(ax, fig, theme, title)
    ax.set_xlabel(xlabel, fontsize=theme['font_size'], fontfamily=theme['font_family'])
    ax.set_ylabel(ylabel, fontsize=theme['font_size'], fontfamily=theme['font_family'])
    
    # Legend
    if line_label or show_outliers or show_forecast or show_trend:
        legend = ax.legend(loc='best', facecolor=theme['background'],
                          edgecolor=theme['grid'], fontsize=theme['font_size'] - 1)
        for text in legend.get_texts():
            text.set_color(theme['text'])
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight',
                   facecolor=theme['figure_bg'])
    
    if show:
        plt.show()
    
    return fig


def styled_bar(
    x: List,
    y: List,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    style: str = DEFAULT_THEME,
    horizontal: bool = False,
    show_values: bool = True,
    color_by_value: bool = False,
    figsize: Tuple[int, int] = (10, 6),
    save_path: str = None,
    show: bool = True
) -> plt.Figure:
    """
    Create a styled bar chart.
    
    Args:
        x: Categories/labels for bars.
        y: Values for each bar.
        title: Chart title.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        style: Theme name.
        horizontal: If True, creates horizontal bar chart.
        show_values: Display value labels on bars.
        color_by_value: Color bars based on their value (gradient).
        figsize: Figure size.
        save_path: Path to save the figure.
        show: Whether to display the plot.
    
    Returns:
        matplotlib Figure object.
    """
    theme = get_theme(style)
    fig, ax = _create_figure(theme, figsize)
    
    x = list(x)
    y = list(y)
    
    # Colors
    if color_by_value:
        norm_y = np.array(y)
        norm_y = (norm_y - norm_y.min()) / (norm_y.max() - norm_y.min() + 1e-10)
        colors = [plt.cm.plasma(v) for v in norm_y]
    else:
        colors = [theme['colors'][i % len(theme['colors'])] for i in range(len(x))]
    
    # Create bars
    if horizontal:
        bars = ax.barh(x, y, color=colors, edgecolor=theme['primary'],
                       linewidth=1.5, height=0.6)
        if show_values:
            for bar, val in zip(bars, y):
                ax.text(bar.get_width() + max(y) * 0.02, bar.get_y() + bar.get_height()/2,
                       f'{val:.1f}', va='center', ha='left',
                       color=theme['text'], fontsize=theme['font_size'] - 1,
                       fontweight='bold')
    else:
        bars = ax.bar(x, y, color=colors, edgecolor=theme['primary'],
                      linewidth=1.5, width=0.6)
        if show_values:
            for bar, val in zip(bars, y):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(y) * 0.02,
                       f'{val:.1f}', ha='center', va='bottom',
                       color=theme['text'], fontsize=theme['font_size'] - 1,
                       fontweight='bold')
    
    _apply_theme(ax, fig, theme, title)
    ax.set_xlabel(xlabel, fontsize=theme['font_size'], fontfamily=theme['font_family'])
    ax.set_ylabel(ylabel, fontsize=theme['font_size'], fontfamily=theme['font_family'])
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight',
                   facecolor=theme['figure_bg'])
    
    if show:
        plt.show()
    
    return fig


def styled_scatter(
    x: List,
    y: List,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    style: str = DEFAULT_THEME,
    sizes: List = None,
    colors: List = None,
    show_outliers: bool = False,
    show_trend: bool = False,
    alpha: float = 0.7,
    figsize: Tuple[int, int] = (10, 6),
    save_path: str = None,
    show: bool = True
) -> plt.Figure:
    """
    Create a styled scatter plot.
    
    Args:
        x: X-axis values.
        y: Y-axis values.
        title: Chart title.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        style: Theme name.
        sizes: Optional list of sizes for each point.
        colors: Optional list of colors for each point.
        show_outliers: Highlight outlier points.
        show_trend: Show regression line.
        alpha: Transparency of points.
        figsize: Figure size.
        save_path: Path to save the figure.
        show: Whether to display the plot.
    
    Returns:
        matplotlib Figure object.
    """
    theme = get_theme(style)
    fig, ax = _create_figure(theme, figsize)
    
    x = list(x)
    y = list(y)
    
    # Default sizes and colors
    if sizes is None:
        sizes = [theme['marker_size']] * len(x)
    if colors is None:
        colors = theme['primary']
    
    # Main scatter
    scatter = ax.scatter(x, y, s=sizes, c=colors, alpha=alpha,
                        edgecolors=theme['secondary'],
                        linewidths=theme['marker_edge_width'],
                        zorder=3)
    
    # Trend line
    if show_trend:
        slope, intercept, direction = calculate_trend(x, y)
        x_line = np.linspace(min(x), max(x), 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color=theme['accent'], linewidth=2,
                linestyle='--', alpha=0.8, label=f'Trend ({direction})')
        ax.legend(loc='best', facecolor=theme['background'],
                 edgecolor=theme['grid']).get_texts()[0].set_color(theme['text'])
    
    # Outliers
    if show_outliers:
        indices, values = detect_outliers(y)
        if indices:
            outlier_x = [x[i] for i in indices]
            ax.scatter(outlier_x, values, s=theme['marker_size'] * 2.5,
                      facecolors='none', edgecolors=theme['accent'],
                      linewidths=3, zorder=5)
    
    _apply_theme(ax, fig, theme, title)
    ax.set_xlabel(xlabel, fontsize=theme['font_size'], fontfamily=theme['font_family'])
    ax.set_ylabel(ylabel, fontsize=theme['font_size'], fontfamily=theme['font_family'])
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight',
                   facecolor=theme['figure_bg'])
    
    if show:
        plt.show()
    
    return fig


def styled_pie(
    values: List,
    labels: List,
    title: str = "",
    style: str = DEFAULT_THEME,
    explode: List = None,
    show_percentages: bool = True,
    donut: bool = False,
    figsize: Tuple[int, int] = (10, 8),
    save_path: str = None,
    show: bool = True
) -> plt.Figure:
    """
    Create a styled pie chart.
    
    Args:
        values: Values for each slice.
        labels: Labels for each slice.
        title: Chart title.
        style: Theme name.
        explode: List of explosion distances for each slice.
        show_percentages: Display percentage on each slice.
        donut: If True, creates a donut chart.
        figsize: Figure size.
        save_path: Path to save the figure.
        show: Whether to display the plot.
    
    Returns:
        matplotlib Figure object.
    """
    theme = get_theme(style)
    fig, ax = _create_figure(theme, figsize)
    
    values = list(values)
    labels = list(labels)
    colors = [theme['colors'][i % len(theme['colors'])] for i in range(len(values))]
    
    if explode is None:
        explode = [0.02] * len(values)
    
    # Create pie
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors, explode=explode,
        autopct='%1.1f%%' if show_percentages else None,
        shadow=False, startangle=90,
        wedgeprops={'edgecolor': theme['background'], 'linewidth': 2}
    )
    
    # Style labels
    for text in texts:
        text.set_color(theme['text'])
        text.set_fontsize(theme['font_size'])
        text.set_fontfamily(theme['font_family'])
    
    if show_percentages:
        for autotext in autotexts:
            autotext.set_color(theme['text'])
            autotext.set_fontsize(theme['font_size'] - 1)
            autotext.set_fontweight('bold')
    
    # Donut hole
    if donut:
        center_circle = plt.Circle((0, 0), 0.5, fc=theme['background'])
        ax.add_patch(center_circle)
    
    ax.axis('equal')
    
    _apply_theme(ax, fig, theme, title)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight',
                   facecolor=theme['figure_bg'])
    
    if show:
        plt.show()
    
    return fig


def styled_histogram(
    data: List,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "Frequency",
    style: str = DEFAULT_THEME,
    bins: int = 'auto',
    show_kde: bool = False,
    show_stats: bool = False,
    figsize: Tuple[int, int] = (10, 6),
    save_path: str = None,
    show: bool = True
) -> plt.Figure:
    """
    Create a styled histogram.
    
    Args:
        data: Data values to histogram.
        title: Chart title.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        style: Theme name.
        bins: Number of bins or 'auto'.
        show_kde: Show kernel density estimate curve.
        show_stats: Display statistics (mean, std) on chart.
        figsize: Figure size.
        save_path: Path to save the figure.
        show: Whether to display the plot.
    
    Returns:
        matplotlib Figure object.
    """
    theme = get_theme(style)
    fig, ax = _create_figure(theme, figsize)
    
    data = np.array(data)
    
    # Create histogram
    n, bins_arr, patches = ax.hist(
        data, bins=bins, color=theme['primary'], alpha=0.7,
        edgecolor=theme['secondary'], linewidth=1.5
    )
    
    # KDE curve
    if show_kde:
        from scipy import stats
        kde = stats.gaussian_kde(data)
        x_kde = np.linspace(data.min(), data.max(), 200)
        y_kde = kde(x_kde) * len(data) * (bins_arr[1] - bins_arr[0])
        ax.plot(x_kde, y_kde, color=theme['accent'], linewidth=2.5,
                label='KDE', zorder=4)
        ax.legend(loc='best', facecolor=theme['background'],
                 edgecolor=theme['grid']).get_texts()[0].set_color(theme['text'])
    
    # Statistics
    if show_stats:
        mean = np.mean(data)
        std = np.std(data)
        ax.axvline(mean, color=theme['accent'], linewidth=2,
                   linestyle='--', label=f'Mean: {mean:.2f}')
        ax.axvspan(mean - std, mean + std, alpha=0.2, color=theme['accent'])
        stats_text = f'μ = {mean:.2f}\nσ = {std:.2f}'
        ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
               fontsize=theme['font_size'], color=theme['text'],
               verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor=theme['background'],
                        edgecolor=theme['grid'], alpha=0.8))
    
    _apply_theme(ax, fig, theme, title)
    ax.set_xlabel(xlabel, fontsize=theme['font_size'], fontfamily=theme['font_family'])
    ax.set_ylabel(ylabel, fontsize=theme['font_size'], fontfamily=theme['font_family'])
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight',
                   facecolor=theme['figure_bg'])
    
    if show:
        plt.show()
    
    return fig


def styled_heatmap(
    data: List[List],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    x_labels: List = None,
    y_labels: List = None,
    style: str = DEFAULT_THEME,
    show_values: bool = True,
    cmap: str = None,
    figsize: Tuple[int, int] = (10, 8),
    save_path: str = None,
    show: bool = True
) -> plt.Figure:
    """
    Create a styled heatmap.
    
    Args:
        data: 2D array of values.
        title: Chart title.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        x_labels: Labels for x-axis ticks.
        y_labels: Labels for y-axis ticks.
        style: Theme name.
        show_values: Display values in cells.
        cmap: Colormap name (uses theme-based default if None).
        figsize: Figure size.
        save_path: Path to save the figure.
        show: Whether to display the plot.
    
    Returns:
        matplotlib Figure object.
    """
    theme = get_theme(style)
    fig, ax = _create_figure(theme, figsize)
    
    data = np.array(data)
    
    # Theme-based colormap
    if cmap is None:
        cmap_dict = {
            'cyberpunk': 'plasma',
            'nordic': 'cool',
            'retro': 'YlOrBr'
        }
        cmap = cmap_dict.get(style, 'viridis')
    
    # Create heatmap
    im = ax.imshow(data, cmap=cmap, aspect='auto')
    
    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.yaxis.set_tick_params(color=theme['text'])
    cbar.outline.set_edgecolor(theme['grid'])
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=theme['text'])
    
    # Labels
    if x_labels is not None:
        ax.set_xticks(np.arange(len(x_labels)))
        ax.set_xticklabels(x_labels)
    if y_labels is not None:
        ax.set_yticks(np.arange(len(y_labels)))
        ax.set_yticklabels(y_labels)
    
    # Values in cells
    if show_values:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                val = data[i, j]
                text_color = 'white' if val > data.mean() else 'black'
                ax.text(j, i, f'{val:.1f}', ha='center', va='center',
                       color=text_color, fontsize=theme['font_size'] - 2,
                       fontweight='bold')
    
    _apply_theme(ax, fig, theme, title)
    ax.set_xlabel(xlabel, fontsize=theme['font_size'], fontfamily=theme['font_family'])
    ax.set_ylabel(ylabel, fontsize=theme['font_size'], fontfamily=theme['font_family'])
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight',
                   facecolor=theme['figure_bg'])
    
    if show:
        plt.show()
    
    return fig
