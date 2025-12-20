"""
FastAPI Backend for enahaplots visualization library.
Provides REST API endpoints to generate charts.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional, Union
import io
import sys
import os

# Add parent directory to path to import enahaplots
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import enahaplots

app = FastAPI(
    title="enahaplots API",
    description="REST API for generating styled charts with enahaplots library",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request Models
# ============================================================

class LineChartRequest(BaseModel):
    x: List[Union[int, float]]
    y: List[Union[int, float]]
    title: str = ""
    xlabel: str = ""
    ylabel: str = ""
    style: str = "cyberpunk"
    show_outliers: bool = False
    show_forecast: bool = False
    forecast_periods: int = 5
    show_trend: bool = False


class BarChartRequest(BaseModel):
    x: List[str]
    y: List[Union[int, float]]
    title: str = ""
    xlabel: str = ""
    ylabel: str = ""
    style: str = "cyberpunk"
    horizontal: bool = False
    show_values: bool = True
    color_by_value: bool = False


class ScatterChartRequest(BaseModel):
    x: List[Union[int, float]]
    y: List[Union[int, float]]
    title: str = ""
    xlabel: str = ""
    ylabel: str = ""
    style: str = "cyberpunk"
    show_outliers: bool = False
    show_trend: bool = False


class PieChartRequest(BaseModel):
    values: List[Union[int, float]]
    labels: List[str]
    title: str = ""
    style: str = "cyberpunk"
    show_percentages: bool = True
    donut: bool = False


class HistogramRequest(BaseModel):
    data: List[Union[int, float]]
    title: str = ""
    xlabel: str = ""
    ylabel: str = "Frequency"
    style: str = "cyberpunk"
    bins: int = 20
    show_stats: bool = False


class HeatmapRequest(BaseModel):
    data: List[List[Union[int, float]]]
    title: str = ""
    xlabel: str = ""
    ylabel: str = ""
    x_labels: Optional[List[str]] = None
    y_labels: Optional[List[str]] = None
    style: str = "cyberpunk"
    show_values: bool = True


# ============================================================
# Helper Functions
# ============================================================

def figure_to_png(fig) -> bytes:
    """Convert matplotlib figure to PNG bytes."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    import matplotlib.pyplot as plt
    plt.close(fig)
    return buf.read()


# ============================================================
# API Endpoints
# ============================================================

@app.get("/")
def root():
    """API health check."""
    return {
        "message": "enahaplots API is running!",
        "version": "1.0.0",
        "themes": enahaplots.list_themes()
    }


@app.get("/api/themes")
def get_themes():
    """Get available themes."""
    return {
        "themes": enahaplots.list_themes(),
        "default": enahaplots.DEFAULT_THEME
    }


@app.post("/api/chart/line")
def create_line_chart(request: LineChartRequest):
    """Generate a styled line chart."""
    try:
        fig = enahaplots.styled_line(
            x=request.x,
            y=request.y,
            title=request.title,
            xlabel=request.xlabel,
            ylabel=request.ylabel,
            style=request.style,
            show_outliers=request.show_outliers,
            show_forecast=request.show_forecast,
            forecast_periods=request.forecast_periods,
            show_trend=request.show_trend,
            show=False
        )
        return Response(content=figure_to_png(fig), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/chart/bar")
def create_bar_chart(request: BarChartRequest):
    """Generate a styled bar chart."""
    try:
        fig = enahaplots.styled_bar(
            x=request.x,
            y=request.y,
            title=request.title,
            xlabel=request.xlabel,
            ylabel=request.ylabel,
            style=request.style,
            horizontal=request.horizontal,
            show_values=request.show_values,
            color_by_value=request.color_by_value,
            show=False
        )
        return Response(content=figure_to_png(fig), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/chart/scatter")
def create_scatter_chart(request: ScatterChartRequest):
    """Generate a styled scatter plot."""
    try:
        fig = enahaplots.styled_scatter(
            x=request.x,
            y=request.y,
            title=request.title,
            xlabel=request.xlabel,
            ylabel=request.ylabel,
            style=request.style,
            show_outliers=request.show_outliers,
            show_trend=request.show_trend,
            show=False
        )
        return Response(content=figure_to_png(fig), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/chart/pie")
def create_pie_chart(request: PieChartRequest):
    """Generate a styled pie chart."""
    try:
        fig = enahaplots.styled_pie(
            values=request.values,
            labels=request.labels,
            title=request.title,
            style=request.style,
            show_percentages=request.show_percentages,
            donut=request.donut,
            show=False
        )
        return Response(content=figure_to_png(fig), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/chart/histogram")
def create_histogram(request: HistogramRequest):
    """Generate a styled histogram."""
    try:
        fig = enahaplots.styled_histogram(
            data=request.data,
            title=request.title,
            xlabel=request.xlabel,
            ylabel=request.ylabel,
            style=request.style,
            bins=request.bins,
            show_stats=request.show_stats,
            show=False
        )
        return Response(content=figure_to_png(fig), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/chart/heatmap")
def create_heatmap(request: HeatmapRequest):
    """Generate a styled heatmap."""
    try:
        fig = enahaplots.styled_heatmap(
            data=request.data,
            title=request.title,
            xlabel=request.xlabel,
            ylabel=request.ylabel,
            x_labels=request.x_labels,
            y_labels=request.y_labels,
            style=request.style,
            show_values=request.show_values,
            show=False
        )
        return Response(content=figure_to_png(fig), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# Math/Analysis Endpoints
# ============================================================

class AnalysisRequest(BaseModel):
    data: List[Union[int, float]]


@app.post("/api/analysis/outliers")
def detect_outliers_endpoint(request: AnalysisRequest):
    """Detect outliers in data."""
    indices, values = enahaplots.detect_outliers(request.data)
    return {"outlier_indices": indices, "outlier_values": values}


@app.post("/api/analysis/statistics")
def calculate_statistics_endpoint(request: AnalysisRequest):
    """Calculate statistics for data."""
    stats = enahaplots.calculate_statistics(request.data)
    return stats


class ForecastRequest(BaseModel):
    x: List[Union[int, float]]
    y: List[Union[int, float]]
    periods: int = 5


@app.post("/api/analysis/forecast")
def forecast_endpoint(request: ForecastRequest):
    """Generate forecast values."""
    fx, fy = enahaplots.forecast(request.x, request.y, request.periods)
    return {"forecast_x": fx, "forecast_y": fy}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
