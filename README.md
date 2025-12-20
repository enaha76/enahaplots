# enahaplots 📊

A personal Python visualization library with beautiful themed charts and built-in statistical analysis.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-purple.svg)

## ✨ Features

- 🎨 **3 Beautiful Themes**: Cyberpunk, Nordic, Retro
- 📈 **6 Chart Types**: Line, Bar, Scatter, Pie, Histogram, Heatmap
- 🧠 **Smart Analysis**: Automatic outlier detection and forecasting
- 📦 **Pip Installable**: Easy installation and usage
- 🌐 **Web Dashboard**: React + FastAPI demo interface

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/YOURUSERNAME/enahaplots.git
cd enahaplots

# Install the library
pip install .
```

---

## 📖 Quick Start

```python
import enahaplots

# Simple line chart
enahaplots.styled_line(
    x=[1, 2, 3, 4, 5],
    y=[10, 20, 15, 25, 30],
    title="My Styled Plot"
)
```

---

## 🎨 Themes

| Theme | Description |
|-------|-------------|
| **Cyberpunk** | Dark background with neon magenta, cyan, yellow |
| **Nordic** | Cool minimalist with frost blue and aurora colors |
| **Retro** | Warm vintage with burnt orange and brown tones |

```python
# Using different themes
enahaplots.styled_bar(x=['A','B','C'], y=[10,20,15], style='nordic')
enahaplots.styled_pie(values=[30,70], labels=['Yes','No'], style='retro')
```

---

## 📊 Chart Types

### Line Chart
```python
enahaplots.styled_line(
    x=[1, 2, 3, 4, 5],
    y=[10, 25, 18, 35, 28],
    title="Sales Trend",
    show_forecast=True,      # Predict future values
    show_outliers=True,      # Highlight anomalies
    show_trend=True          # Display trend line
)
```

### Bar Chart
```python
enahaplots.styled_bar(
    x=["Product A", "Product B", "Product C"],
    y=[45, 72, 58],
    title="Product Sales",
    horizontal=True,         # Horizontal bars
    show_values=True         # Display value labels
)
```

### Scatter Plot
```python
enahaplots.styled_scatter(
    x=[1, 2, 3, 4, 5],
    y=[2, 4, 5, 8, 9],
    title="Correlation",
    show_trend=True          # Regression line
)
```

### Pie / Donut Chart
```python
enahaplots.styled_pie(
    values=[35, 25, 20, 15, 5],
    labels=["Chrome", "Safari", "Firefox", "Edge", "Other"],
    title="Browser Share",
    donut=True               # Donut style
)
```

### Histogram
```python
import random
data = [random.gauss(50, 15) for _ in range(200)]

enahaplots.styled_histogram(
    data=data,
    title="Score Distribution",
    show_stats=True          # Show mean/std
)
```

### Heatmap
```python
enahaplots.styled_heatmap(
    data=[[10, 20], [30, 40]],
    title="Correlation Matrix",
    x_labels=["A", "B"],
    y_labels=["X", "Y"]
)
```

---

## 🧠 Smart Features

### Outlier Detection
Automatically identifies and highlights unusual data points using Z-score method.

### Forecasting
Predicts future values using linear regression.

```python
enahaplots.styled_line(
    x=[1, 2, 3, 4, 5],
    y=[100, 120, 140, 160, 180],
    show_forecast=True,
    forecast_periods=3       # Predict 3 future periods
)
```

---

## 🌐 Web Dashboard (Bonus)

Run the interactive dashboard with React + FastAPI:

### Start Backend
```bash
cd backend
source venv/bin/activate  # or: python -m venv venv && pip install -r requirements.txt
uvicorn main:app --reload
```

### Start Frontend
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 📁 Project Structure

```
enahaplots/
├── enahaplots/          # Python library
│   ├── __init__.py
│   ├── themes.py        # Theme configurations
│   ├── math_engine.py   # Statistical functions
│   └── plots.py         # Chart functions
├── backend/             # FastAPI server
├── frontend/            # React dashboard
├── examples/            # Demo scripts
├── pyproject.toml       # Package config
└── setup.py
```

---

## 📜 License

MIT License

---

## 👤 Author

**Enaha**

---

## 🙏 Acknowledgments

Built with:
- [Matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
