"""
Demo script for enahaplots library.
Shows all chart types with different themes and features.
"""

import enahaplots

# ============================================================
# DEMO 1: Basic Line Chart (Cyberpunk theme - default)
# ============================================================
print("Demo 1: Basic Line Chart")
enahaplots.styled_line(
    x=[1, 2, 3, 4, 5, 6, 7],
    y=[10, 25, 18, 35, 28, 42, 38],
    title="Sales Trend - Cyberpunk Theme",
    xlabel="Month",
    ylabel="Sales (K$)",
    style="cyberpunk"
)

# ============================================================
# DEMO 2: Line Chart with Outliers & Forecast (Nordic theme)
# ============================================================
print("Demo 2: Line Chart with Smart Features")
enahaplots.styled_line(
    x=[1, 2, 3, 4, 5, 6, 7, 8],
    y=[100, 120, 115, 130, 250, 140, 135, 145],  # 250 is outlier
    title="Revenue Analysis with Forecast",
    xlabel="Quarter",
    ylabel="Revenue (M$)",
    style="nordic",
    show_outliers=True,
    show_forecast=True,
    forecast_periods=3,
    show_trend=True
)

# ============================================================
# DEMO 3: Bar Chart (Retro theme)
# ============================================================
print("Demo 3: Bar Chart")
enahaplots.styled_bar(
    x=["Product A", "Product B", "Product C", "Product D", "Product E"],
    y=[45, 72, 58, 91, 67],
    title="Product Performance - Retro Theme",
    xlabel="Products",
    ylabel="Units Sold",
    style="retro",
    show_values=True,
    color_by_value=True
)

# ============================================================
# DEMO 4: Horizontal Bar Chart
# ============================================================
print("Demo 4: Horizontal Bar Chart")
enahaplots.styled_bar(
    x=["Python", "JavaScript", "Go", "Rust", "Java"],
    y=[92, 85, 78, 71, 65],
    title="Programming Language Popularity",
    xlabel="Popularity Score",
    ylabel="Language",
    style="cyberpunk",
    horizontal=True,
    show_values=True
)

# ============================================================
# DEMO 5: Scatter Plot with Trend (Nordic theme)
# ============================================================
print("Demo 5: Scatter Plot")
import random
random.seed(42)
x_data = list(range(1, 21))
y_data = [x * 2 + random.randint(-5, 5) for x in x_data]

enahaplots.styled_scatter(
    x=x_data,
    y=y_data,
    title="Correlation Analysis",
    xlabel="Variable X",
    ylabel="Variable Y",
    style="nordic",
    show_trend=True,
    show_outliers=True
)

# ============================================================
# DEMO 6: Pie Chart (Cyberpunk theme)
# ============================================================
print("Demo 6: Pie Chart")
enahaplots.styled_pie(
    values=[35, 25, 20, 15, 5],
    labels=["Chrome", "Safari", "Firefox", "Edge", "Other"],
    title="Browser Market Share",
    style="cyberpunk",
    show_percentages=True
)

# ============================================================
# DEMO 7: Donut Chart (Retro theme)
# ============================================================
print("Demo 7: Donut Chart")
enahaplots.styled_pie(
    values=[40, 30, 20, 10],
    labels=["Desktop", "Mobile", "Tablet", "Other"],
    title="Device Usage - Donut Style",
    style="retro",
    donut=True,
    show_percentages=True
)

# ============================================================
# DEMO 8: Histogram with Stats (Nordic theme)
# ============================================================
print("Demo 8: Histogram")
import random
random.seed(123)
data = [random.gauss(50, 15) for _ in range(200)]

enahaplots.styled_histogram(
    data=data,
    title="Score Distribution",
    xlabel="Score",
    ylabel="Frequency",
    style="nordic",
    bins=20,
    show_stats=True
)

# ============================================================
# DEMO 9: Heatmap (Cyberpunk theme)
# ============================================================
print("Demo 9: Heatmap")
heatmap_data = [
    [10, 20, 30, 40],
    [15, 25, 35, 45],
    [20, 30, 40, 50],
    [25, 35, 45, 55]
]

enahaplots.styled_heatmap(
    data=heatmap_data,
    title="Correlation Matrix",
    x_labels=["A", "B", "C", "D"],
    y_labels=["W", "X", "Y", "Z"],
    style="cyberpunk",
    show_values=True
)

print("\n✅ All demos completed successfully!")
print("📊 enahaplots is working correctly.")
