import { useState } from 'react'

// Chart types configuration
const CHART_TYPES = [
    { id: 'line', icon: '📈', label: 'Line' },
    { id: 'bar', icon: '📊', label: 'Bar' },
    { id: 'scatter', icon: '⚬', label: 'Scatter' },
    { id: 'pie', icon: '🥧', label: 'Pie' },
    { id: 'histogram', icon: '📶', label: 'Histogram' },
    { id: 'heatmap', icon: '🟦', label: 'Heatmap' },
]

const THEMES = ['cyberpunk', 'nordic', 'retro']

// Sample data for different chart types
const SAMPLE_DATA: Record<string, object> = {
    line: {
        x: [1, 2, 3, 4, 5, 6, 7, 8],
        y: [10, 25, 18, 35, 28, 45, 38, 52],
        title: 'Sales Trend Analysis',
        xlabel: 'Month',
        ylabel: 'Revenue (K$)',
    },
    bar: {
        x: ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
        y: [45, 72, 58, 91, 67],
        title: 'Product Performance',
        xlabel: 'Products',
        ylabel: 'Units Sold',
    },
    scatter: {
        x: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        y: [2, 4, 5, 8, 9, 12, 14, 15, 18, 21, 23, 25, 28, 30, 32],
        title: 'Correlation Analysis',
        xlabel: 'Variable X',
        ylabel: 'Variable Y',
    },
    pie: {
        values: [35, 25, 20, 15, 5],
        labels: ['Chrome', 'Safari', 'Firefox', 'Edge', 'Other'],
        title: 'Browser Market Share',
    },
    histogram: {
        data: Array.from({ length: 100 }, () => Math.random() * 100),
        title: 'Score Distribution',
        xlabel: 'Score',
        ylabel: 'Frequency',
        bins: 20,
    },
    heatmap: {
        data: [
            [10, 20, 30, 40],
            [15, 25, 35, 45],
            [20, 30, 40, 50],
            [25, 35, 45, 55],
        ],
        title: 'Correlation Matrix',
        x_labels: ['A', 'B', 'C', 'D'],
        y_labels: ['W', 'X', 'Y', 'Z'],
    },
}

function App() {
    const [chartType, setChartType] = useState('line')
    const [theme, setTheme] = useState('cyberpunk')
    const [chartImage, setChartImage] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    // Options for line chart
    const [showOutliers, setShowOutliers] = useState(false)
    const [showForecast, setShowForecast] = useState(false)
    const [showTrend, setShowTrend] = useState(false)

    // Options for bar chart
    const [horizontal, setHorizontal] = useState(false)
    const [showValues, setShowValues] = useState(true)
    const [colorByValue, setColorByValue] = useState(false)

    // Options for pie chart
    const [donut, setDonut] = useState(false)
    const [showPercentages, setShowPercentages] = useState(true)

    // Options for histogram
    const [showStats, setShowStats] = useState(false)

    const generateChart = async () => {
        setLoading(true)
        setError(null)

        try {
            const baseData = SAMPLE_DATA[chartType]
            let requestData = { ...baseData, style: theme }

            // Add options based on chart type
            if (chartType === 'line') {
                requestData = {
                    ...requestData,
                    show_outliers: showOutliers,
                    show_forecast: showForecast,
                    show_trend: showTrend,
                }
            } else if (chartType === 'bar') {
                requestData = {
                    ...requestData,
                    horizontal,
                    show_values: showValues,
                    color_by_value: colorByValue,
                }
            } else if (chartType === 'scatter') {
                requestData = {
                    ...requestData,
                    show_outliers: showOutliers,
                    show_trend: showTrend,
                }
            } else if (chartType === 'pie') {
                requestData = {
                    ...requestData,
                    donut,
                    show_percentages: showPercentages,
                }
            } else if (chartType === 'histogram') {
                requestData = {
                    ...requestData,
                    show_stats: showStats,
                }
            }

            const response = await fetch(`/api/chart/${chartType}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            })

            if (!response.ok) {
                throw new Error(`Failed to generate chart: ${response.statusText}`)
            }

            const blob = await response.blob()
            const imageUrl = URL.createObjectURL(blob)
            setChartImage(imageUrl)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred')
        } finally {
            setLoading(false)
        }
    }

    const renderOptions = () => {
        switch (chartType) {
            case 'line':
                return (
                    <div className="checkbox-group">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={showOutliers}
                                onChange={(e) => setShowOutliers(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">🔴 Highlight Outliers</span>
                        </label>
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={showForecast}
                                onChange={(e) => setShowForecast(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">🔮 Show Forecast</span>
                        </label>
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={showTrend}
                                onChange={(e) => setShowTrend(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">📈 Show Trend Line</span>
                        </label>
                    </div>
                )

            case 'bar':
                return (
                    <div className="checkbox-group">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={horizontal}
                                onChange={(e) => setHorizontal(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">↔️ Horizontal Bars</span>
                        </label>
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={showValues}
                                onChange={(e) => setShowValues(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">🔢 Show Values</span>
                        </label>
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={colorByValue}
                                onChange={(e) => setColorByValue(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">🌈 Color by Value</span>
                        </label>
                    </div>
                )

            case 'scatter':
                return (
                    <div className="checkbox-group">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={showOutliers}
                                onChange={(e) => setShowOutliers(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">🔴 Highlight Outliers</span>
                        </label>
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={showTrend}
                                onChange={(e) => setShowTrend(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">📈 Show Regression Line</span>
                        </label>
                    </div>
                )

            case 'pie':
                return (
                    <div className="checkbox-group">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={donut}
                                onChange={(e) => setDonut(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">🍩 Donut Style</span>
                        </label>
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={showPercentages}
                                onChange={(e) => setShowPercentages(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">% Show Percentages</span>
                        </label>
                    </div>
                )

            case 'histogram':
                return (
                    <div className="checkbox-group">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={showStats}
                                onChange={(e) => setShowStats(e.target.checked)}
                            />
                            <span className="checkbox-custom"></span>
                            <span className="checkbox-text">📊 Show Statistics</span>
                        </label>
                    </div>
                )

            default:
                return null
        }
    }

    return (
        <div className="app">
            <header className="header">
                <div className="logo">
                    <div className="logo-icon">📊</div>
                    <h1>enahaplots</h1>
                </div>
                <span style={{ color: 'var(--text-muted)' }}>
                    Interactive Chart Dashboard
                </span>
            </header>

            <main className="main-content">
                <aside className="sidebar">
                    {/* Chart Type Selector */}
                    <div className="card">
                        <h2 className="card-title">Chart Type</h2>
                        <div className="chart-type-grid">
                            {CHART_TYPES.map((type) => (
                                <button
                                    key={type.id}
                                    className={`chart-type-btn ${chartType === type.id ? 'active' : ''}`}
                                    onClick={() => setChartType(type.id)}
                                >
                                    <span className="icon">{type.icon}</span>
                                    <span className="label">{type.label}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Theme Selector */}
                    <div className="card">
                        <h2 className="card-title">Theme</h2>
                        <div className="theme-selector">
                            {THEMES.map((t) => (
                                <button
                                    key={t}
                                    className={`theme-option theme-${t} ${theme === t ? 'active' : ''}`}
                                    onClick={() => setTheme(t)}
                                >
                                    <div className="theme-preview">
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                    </div>
                                    <span className="theme-name">{t}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Options */}
                    <div className="card">
                        <h2 className="card-title">Options</h2>
                        {renderOptions()}
                    </div>

                    {/* Generate Button */}
                    <button
                        className="btn btn-primary btn-full"
                        onClick={generateChart}
                        disabled={loading}
                    >
                        {loading ? 'Generating...' : '✨ Generate Chart'}
                    </button>

                    {error && (
                        <div
                            className="card"
                            style={{ borderColor: 'var(--accent-warning)' }}
                        >
                            <p style={{ color: 'var(--accent-warning)' }}>⚠️ {error}</p>
                            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
                                Make sure the FastAPI backend is running on port 8000
                            </p>
                        </div>
                    )}
                </aside>

                <section className="chart-container">
                    <div className="chart-display">
                        {loading ? (
                            <div className="loading">
                                <div className="spinner"></div>
                                <p>Generating your chart...</p>
                            </div>
                        ) : chartImage ? (
                            <img
                                src={chartImage}
                                alt="Generated chart"
                                className="chart-image"
                            />
                        ) : (
                            <div className="chart-placeholder">
                                <div className="chart-placeholder-icon">📊</div>
                                <h3>No Chart Generated</h3>
                                <p>Select a chart type, theme, and options, then click Generate</p>
                            </div>
                        )}
                    </div>
                </section>
            </main>
        </div>
    )
}

export default App
