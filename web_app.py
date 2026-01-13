/* General dashboard styling */
body {
    font-family: "Segoe UI", Arial, sans-serif;
    color: var(--text-color); /* adapts to theme */
}

/* Main page title (# in Streamlit -> <h1>) */
h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    margin-bottom: 1rem !important;
    margin-top: 0.5rem !important;
    color: var(--text-color) !important;
    line-height: 1.2 !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
}

/* Main section titles (## in Streamlit -> <h2>) */
h2 {
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    margin-bottom: 1.5rem !important;
    margin-top: 0.5rem !important;
    color: var(--text-color) !important;
    line-height: 1.2 !important;
}

/* Section headings (### in Streamlit -> <h3>) - styled as h5 */
h3 {
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
    margin-top: 0.75rem !important;
    color: var(--text-color) !important;
    line-height: 1.5 !important;
}

/* Consistent heading styles across all tabs */
h4 {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.75rem !important;
    margin-top: 1rem !important;
    color: var(--text-color) !important;
    line-height: 1.4 !important;
}

/* Subsection headings (h5) */
h5 {
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
    margin-top: 0.75rem !important;
    color: var(--text-color) !important;
    line-height: 1.5 !important;
}

/* Metric labels and values */
.metric-label {
    font-size: 14px;
    font-weight: bold;
    color: var(--text-color);
}
.metric-value {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-color);
}

/* Plotly chart text overrides */
.js-plotly-plot .main-svg text.gtitle,
.js-plotly-plot .main-svg text.xtitle,
.js-plotly-plot .main-svg text.ytitle,
.js-plotly-plot .main-svg text.xtick,
.js-plotly-plot .main-svg text.ytick,
.js-plotly-plot .main-svg text.legendtext {
    fill: var(--text-color) !important;
    color: var(--text-color) !important;
}

/* Override Streamlit's st.metric widget globally */
[data-testid="stMetricValue"] {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: var(--text-color) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 14px !important;
    font-weight: bold !important;
    color: var(--text-color) !important;
}

/* Removed fixed chart height clamp
   Let Python control chart height dynamically */

/* Chart titles */
.plotly-title,
.js-plotly-plot .main-svg text.gtitle {
    font-size: 16px !important;
    font-weight: bold !important;
    fill: var(--text-color) !important;
    color: var(--text-color) !important;
    text-anchor: middle !important;
}

/* Axis titles */
.plotly-axis-title,
.js-plotly-plot .main-svg text.xtitle,
.js-plotly-plot .main-svg text.ytitle {
    font-size: 12px !important;
    font-weight: 500 !important;
    fill: var(--text-color) !important;
    color: var(--text-color) !important;
}

/* Tick labels */
.plotly-tick-label,
.js-plotly-plot .main-svg text.xtick,
.js-plotly-plot .main-svg text.ytick {
    font-size: 10px !important;
    fill: var(--text-color) !important;
    color: var(--text-color) !important;
}

/* Reduce Streamlit container padding */
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
}

/* Sidebar styling */
.css-1d391kg {
    font-size: 13px;
    color: var(--text-color);
}

/* Tabs styling */
.stTabs [role="tab"] {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-color);
}

/* Ensure header action elements don't affect size */
.st-emotion-cache-gi0tri {
    display: inline-block !important;
}

/* Tab consistency */
.stTabs [data-baseweb="tab-list"] button {
    font-size: 1rem !important;
    font-weight: 500 !important;
}

/* Chart container adjustments for better spacing */
.js-plotly-plot {
    margin-left: 10px !important;
}

/* Ensure plotly chart SVG has adequate padding */
.plotly .main-svg {
    overflow: visible !important;
}

/* Y-axis title spacing */
.js-plotly-plot .main-svg g.g-ytitle {
    transform: translateX(-10px) !important;
}

/* Thicker container borders - increased to 5px for maximum visibility */
[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
    border-width: 5px !important;
}

div[data-testid="stVerticalBlock"] > div[style*="border"] {
    border-width: 5px !important;
}

/* Make all bordered containers thicker */
div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] {
    border-width: 5px !important;
}

/* Additional container border styling */
[data-testid="stVerticalBlock"][style*="border"] {
    border-width: 5px !important;
}
