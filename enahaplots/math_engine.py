# enahaplots/math_engine.py
"""
Mathematical analysis engine for enahaplots.
Provides outlier detection and forecasting capabilities.
"""

import numpy as np
from typing import Tuple, List, Optional


def detect_outliers(data: list, method: str = 'zscore', threshold: float = 2.0) -> Tuple[list, list]:
    """
    Detect outliers in a dataset.
    
    Args:
        data: List or array of numerical values.
        method: Detection method - 'zscore' or 'iqr'.
        threshold: For zscore method, number of standard deviations (default 2.0).
                   For IQR method, multiplier for IQR (default 1.5).
    
    Returns:
        Tuple of (outlier_indices, outlier_values)
    """
    arr = np.array(data, dtype=float)
    
    if method == 'zscore':
        mean = np.mean(arr)
        std = np.std(arr)
        if std == 0:
            return [], []
        z_scores = np.abs((arr - mean) / std)
        outlier_mask = z_scores > threshold
    
    elif method == 'iqr':
        q1 = np.percentile(arr, 25)
        q3 = np.percentile(arr, 75)
        iqr = q3 - q1
        lower_bound = q1 - (threshold * iqr)
        upper_bound = q3 + (threshold * iqr)
        outlier_mask = (arr < lower_bound) | (arr > upper_bound)
    
    else:
        raise ValueError(f"Unknown method: {method}. Use 'zscore' or 'iqr'.")
    
    outlier_indices = np.where(outlier_mask)[0].tolist()
    outlier_values = arr[outlier_mask].tolist()
    
    return outlier_indices, outlier_values


def calculate_trend(x: list, y: list) -> Tuple[float, float, str]:
    """
    Calculate the linear trend of data.
    
    Args:
        x: X-axis values (can be indices if not provided).
        y: Y-axis values.
    
    Returns:
        Tuple of (slope, intercept, trend_direction)
        trend_direction is 'up', 'down', or 'flat'
    """
    x_arr = np.array(x, dtype=float)
    y_arr = np.array(y, dtype=float)
    
    # Linear regression using least squares
    coefficients = np.polyfit(x_arr, y_arr, 1)
    slope = coefficients[0]
    intercept = coefficients[1]
    
    # Determine trend direction
    if slope > 0.01:
        direction = 'up'
    elif slope < -0.01:
        direction = 'down'
    else:
        direction = 'flat'
    
    return float(slope), float(intercept), direction


def forecast(x: list, y: list, periods: int = 5) -> Tuple[list, list]:
    """
    Generate forecast values using linear regression.
    
    Args:
        x: Historical X-axis values (typically time indices).
        y: Historical Y-axis values.
        periods: Number of future periods to forecast.
    
    Returns:
        Tuple of (forecast_x, forecast_y) containing the predicted values.
    """
    x_arr = np.array(x, dtype=float)
    y_arr = np.array(y, dtype=float)
    
    # Fit linear model
    slope, intercept, _ = calculate_trend(x, y)
    
    # Generate future x values
    if len(x_arr) > 1:
        step = x_arr[-1] - x_arr[-2]
    else:
        step = 1
    
    forecast_x = [float(x_arr[-1] + step * (i + 1)) for i in range(periods)]
    forecast_y = [float(slope * fx + intercept) for fx in forecast_x]
    
    return forecast_x, forecast_y


def calculate_statistics(data: list) -> dict:
    """
    Calculate comprehensive statistics for a dataset.
    
    Args:
        data: List of numerical values.
    
    Returns:
        Dictionary containing: mean, median, std, min, max, range, q1, q3
    """
    arr = np.array(data, dtype=float)
    
    return {
        'mean': float(np.mean(arr)),
        'median': float(np.median(arr)),
        'std': float(np.std(arr)),
        'min': float(np.min(arr)),
        'max': float(np.max(arr)),
        'range': float(np.max(arr) - np.min(arr)),
        'q1': float(np.percentile(arr, 25)),
        'q3': float(np.percentile(arr, 75)),
        'count': len(arr)
    }


def moving_average(data: list, window: int = 3) -> list:
    """
    Calculate moving average of data.
    
    Args:
        data: List of numerical values.
        window: Size of the moving window.
    
    Returns:
        List of moving average values (shorter than input by window-1).
    """
    arr = np.array(data, dtype=float)
    
    if window > len(arr):
        window = len(arr)
    
    cumsum = np.cumsum(np.insert(arr, 0, 0))
    return ((cumsum[window:] - cumsum[:-window]) / window).tolist()


def normalize(data: list, method: str = 'minmax') -> list:
    """
    Normalize data to a standard range.
    
    Args:
        data: List of numerical values.
        method: 'minmax' (0-1 range) or 'zscore' (standard normal).
    
    Returns:
        List of normalized values.
    """
    arr = np.array(data, dtype=float)
    
    if method == 'minmax':
        min_val = np.min(arr)
        max_val = np.max(arr)
        if max_val - min_val == 0:
            return [0.5] * len(arr)
        return ((arr - min_val) / (max_val - min_val)).tolist()
    
    elif method == 'zscore':
        mean = np.mean(arr)
        std = np.std(arr)
        if std == 0:
            return [0.0] * len(arr)
        return ((arr - mean) / std).tolist()
    
    else:
        raise ValueError(f"Unknown method: {method}. Use 'minmax' or 'zscore'.")
