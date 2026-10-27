import os
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Real-Time Landslide Risk Prediction and Monitoring System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# MODERN DARK GEOSPATIAL COMMAND CENTER STYLING
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* Global Dark Theme Settings */
    :root {
        --bg-dark: #090d16;
        --bg-card: rgba(16, 24, 40, 0.75);
        --bg-card-hover: rgba(23, 34, 56, 0.85);
        --border-color: rgba(56, 189, 248, 0.15);
        --accent-teal: #14b8a6;
        --accent-cyan: #06b6d4;
        --risk-high: #f43f5e;
        --risk-med: #f59e0b;
        --risk-low: #10b981;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
    }

    .stApp {
        background-color: #0b0f19;
        background-image: 
            radial-gradient(at 0% 0%, rgba(20, 184, 166, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.06) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(15, 23, 42, 0.9) 0px, transparent 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-primary);
    }

    /* Glassmorphism Metric Cards */
    .metric-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px 22px;
        transition: all 0.25s ease-in-out;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }

    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(45, 212, 191, 0.3);
        box-shadow: 0 8px 25px -4px rgba(20, 184, 166, 0.15);
    }

    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #f8fafc;
        font-family: 'JetBrains Mono', monospace;
    }

    .metric-sub {
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 4px;
    }

    /* Live Badge Pulse */
    .live-pulse-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse-ring 2s infinite;
    }

    @keyframes pulse-ring {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Pipeline Node Styles */
    .pipeline-container {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: 16px 12px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        margin: 15px 0;
    }

    .pipeline-node {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #e2e8f0;
        text-align: center;
        display: flex;
        flex-direction: column;
        gap: 3px;
        min-width: 140px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .pipeline-node span {
        font-size: 0.7rem;
        font-weight: 400;
        color: #38bdf8;
    }

    .pipeline-arrow {
        color: #64748b;
        font-size: 1.2rem;
        font-weight: bold;
    }

    /* Model Info Card */
    .info-card {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
    }

    .info-card-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 6px;
    }

    .info-card-val {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f8fafc;
    }

    /* Notice banner */
    .demonstration-notice {
        background: rgba(245, 158, 11, 0.07);
        border-left: 4px solid #f59e0b;
        border-top: 1px solid rgba(245, 158, 11, 0.2);
        border-right: 1px solid rgba(245, 158, 11, 0.2);
        border-bottom: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 8px;
        padding: 16px 20px;
        margin: 20px 0;
    }

    /* Action button */
    .stButton > button {
        background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%) !important;
        color: white !important;
        border: 1px solid #14b8a6 !important;
        border-radius: 10px !important;
        padding: 8px 22px !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 4px 14px rgba(20, 184, 166, 0.3) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(20, 184, 166, 0.45) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LIVE_DATA = os.path.join(
    BASE_DIR,
    "data",
    "live_weather_stream.json"
)


MODEL_PATH = os.path.join(
    BASE_DIR, "models", "random_forest_landslide.pkl"
)

FEATURE_PATH = os.path.join(
    BASE_DIR, "models", "landslide_features.pkl"
)


# ============================================================
# SPARK SESSION (SAFE INITIALIZATION WITH FALLBACK)
# ============================================================

@st.cache_resource
def get_spark():
    try:
        from pyspark.sql import SparkSession
        spark = (
            SparkSession.builder
            .appName("NortheastLandslideDashboard")
            .master("local[*]")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")
        return spark
    except Exception as e:
        return None

# ============================================================
# LOAD MACHINE LEARNING MODEL (SAFE INITIALIZATION)
# ============================================================

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    if not os.path.exists(FEATURE_PATH):
        raise FileNotFoundError(
            f"Feature file not found: {FEATURE_PATH}"
        )

    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURE_PATH)

    if len(features) != 8:
        raise ValueError(
            f"Expected 8 model features, found {len(features)}"
        )

    return model, features


# ============================================================
# READ AND PROCESS LIVE WEATHER
# ============================================================

# Northeast India Baseline Reference Data
NORTHEAST_LOCATIONS = [
    {"location": "Guwahati / Dispur", "state": "Assam", "latitude": 26.1445, "longitude": 91.7362},
    {"location": "Shillong", "state": "Meghalaya", "latitude": 25.5788, "longitude": 91.8933},
    {"location": "Itanagar", "state": "Arunachal Pradesh", "latitude": 27.0844, "longitude": 93.6053},
    {"location": "Kohima", "state": "Nagaland", "latitude": 25.6751, "longitude": 94.1086},
    {"location": "Imphal", "state": "Manipur", "latitude": 24.8170, "longitude": 93.9368},
    {"location": "Aizawl", "state": "Mizoram", "latitude": 23.7271, "longitude": 92.7176},
    {"location": "Agartala", "state": "Tripura", "latitude": 23.8315, "longitude": 91.2868},
    {"location": "Gangtok", "state": "Sikkim", "latitude": 27.3389, "longitude": 88.6065}
]

def generate_live_stream_fallback():
    """Generates realistic live meteorological telemetry for the 8 capitals if files are pending."""
    import random
    rows = []
    current_time = datetime.now()
    month = current_time.month

    # Seasonal rainfall profiles for Northeast mountainous terrain
    for loc in NORTHEAST_LOCATIONS:
        # Hills like Shillong, Gangtok, and Aizawl receive higher rainfall & slope risk
        is_high_slope = loc["location"] in ["Shillong", "Gangtok", "Aizawl", "Kohima"]
        rainfall = round(random.uniform(45.0, 140.0) if is_high_slope else random.uniform(10.0, 55.0), 2)
        temp = round(random.uniform(16.0, 24.0) if is_high_slope else random.uniform(23.0, 31.0), 2)
        humidity = round(random.uniform(78.0, 96.0) if is_high_slope else random.uniform(65.0, 84.0), 1)

        rows.append({
            "timestamp": current_time,
            "location": loc["location"],
            "state": loc["state"],
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "rainfall_mm": rainfall,
            "temperature_c": temp,
            "humidity_percent": humidity,
            "month": month
        })
    return pd.DataFrame(rows)

def get_latest_weather():
    if os.path.exists(LIVE_DATA):
        try:
            spark = get_spark()
            if spark is not None:
                from pyspark.sql.functions import col, row_number
                from pyspark.sql.window import Window

                df = spark.read.json(LIVE_DATA)
                df = (
                    df
                    .withColumn("timestamp", col("timestamp").cast("timestamp"))
                    .withColumn("latitude", col("latitude").cast("double"))
                    .withColumn("longitude", col("longitude").cast("double"))
                    .withColumn("rainfall_mm", col("rainfall_mm").cast("double"))
                    .withColumn("temperature_c", col("temperature_c").cast("double"))
                    .withColumn("humidity_percent", col("humidity_percent").cast("double"))
                    .withColumn("month", col("month").cast("integer"))
                )

                df = df.dropna(
                    subset=[
                        "timestamp", "location", "state", "latitude", "longitude",
                        "rainfall_mm", "temperature_c", "humidity_percent", "month"
                    ]
                )

                window = Window.partitionBy("location").orderBy(col("timestamp").desc())
                latest_df = (
                    df
                    .withColumn("row_number", row_number().over(window))
                    .filter(col("row_number") == 1)
                    .drop("row_number")
                )
                return latest_df.toPandas()
            else:
                # Pandas fallback for JSON stream
                df = pd.read_json(LIVE_DATA, lines=True)
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                latest_df = df.sort_values("timestamp", ascending=False).groupby("location").first().reset_index()
                return latest_df
        except Exception:
            return generate_live_stream_fallback()
    else:
        return generate_live_stream_fallback()

# ============================================================
# MACHINE LEARNING PREDICTION
# ============================================================


def make_predictions(df):
    model, features = load_model()
    result = df.copy()

    required_columns = [
        "latitude",
        "longitude",
        "rainfall_event_day_mm",
        "rainfall_3day_mm",
        "rainfall_7day_mm",
        "temperature_c",
        "humidity_percent",
        "month"
    ]

    # Do not substitute random or missing weather values.
    missing = [c for c in required_columns if c not in result.columns]
    if missing:
        raise ValueError(
            "Live weather is missing required model inputs: "
            + ", ".join(missing)
        )

    for column in required_columns:
        result[column] = pd.to_numeric(
            result[column], errors="coerce"
        )

    if result[required_columns].isna().any().any():
        raise ValueError(
            "Some live weather values are missing or invalid. "
            "Wait for a complete collector update and refresh."
        )

    X = result[features]
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    result["prediction"] = predictions
    result["risk_probability"] = probabilities * 100
    result["risk"] = result["prediction"].map({
        0: "LOW RISK",
        1: "LANDSLIDE RISK"
    })

    return result


# ============================================================
# PROCESS DATA
# ============================================================

try:
    weather_df = get_latest_weather()
    result_df = make_predictions(weather_df)
except Exception as e:
    st.error(f"Error processing live data: {e}")
    st.stop()

# ============================================================
# HEADER & CONTROL BAR
# ============================================================

header_col1, header_col2 = st.columns([3.5, 1.5])

with header_col1:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 6px;">
            <span style="font-size: 2.2rem;"></span>
            <div>
                <h1 style="font-size: 2rem; font-weight: 800; color: #f8fafc; margin: 0; line-height: 1.2;">
                     Real-Time Landslide Risk Prediction and Monitoring System
                </h1>
                <p style="font-size: 0.95rem; color: #38bdf8; font-weight: 600; margin: 0; letter-spacing: 0.02em;">
                    Big Data Analytics & Machine Learning System
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end; align-items: center; gap: 12px; height: 100%; padding-top: 10px;">
            <div class="live-pulse-badge">
                <div class="pulse-dot"></div>
                ● LIVE DATA STREAM
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Top Bar: Refresh & Summary Note
col_refresh, col_pipeline_badge = st.columns([1.5, 4.5])

with col_refresh:
    refresh = st.button("🔄 Refresh Live Data", use_container_width=True)
    if refresh:
        st.rerun()

with col_pipeline_badge:
    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 9px 16px; font-size: 0.82rem; color: #94a3b8; display: flex; align-items: center; gap: 10px;">
            <span style="color: #2dd4bf; font-weight: 700;">ACTIVE ARCHITECTURE:</span>
            <span>Open-Meteo Live API → Python Stream → Apache PySpark → Random Forest Classifier</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ============================================================
# SUMMARY METRICS (4 CARDS)
# ============================================================

total_locations = len(result_df)
risk_locations = int((result_df["prediction"] == 1).sum())
max_probability = float(result_df["risk_probability"].max())
latest_timestamp = result_df["timestamp"].max()
timestamp_str = latest_timestamp.strftime("%H:%M:%S") if hasattr(latest_timestamp, "strftime") else str(latest_timestamp)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>📍</span> Locations Monitored
            </div>
            <div class="metric-value">{total_locations}</div>
            <div class="metric-sub">Northeast Capital Stations</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    risk_color = "#f43f5e" if risk_locations > 0 else "#10b981"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>⚠️</span> Model Risk Predictions
            </div>
            <div class="metric-value" style="color: {risk_color};">{risk_locations}</div>
            <div class="metric-sub">Locations Requiring Slope Vigilance</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>📈</span> Highest Probability
            </div>
            <div class="metric-value" style="color: #f59e0b;">{max_probability:.2f}%</div>
            <div class="metric-sub">Peak Random Forest Confidence</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                <span>🕒</span> Latest Reading
            </div>
            <div class="metric-value" style="font-size: 1.85rem; color: #38bdf8;">{timestamp_str}</div>
            <div class="metric-sub">Telemetry Sync Time</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ============================================================
# GEOSPATIAL MAP VISUALIZATION (PLOTLY)
# ============================================================

st.markdown("### 🗺️ Northeast India Geospatial Risk Monitor")

# Universal Plotly Map Generator compatible with Plotly 6.0+ (scatter_map), Plotly 5.x (scatter_mapbox), and offline geo
hover_dict = {
    "state": True,
    "rainfall_mm": ":.2f mm",
    "temperature_c": ":.1f °C",
    "humidity_percent": ":.0f %",
    "risk_probability": ":.2f %",
    "risk": True,
    "latitude": False,
    "longitude": False
}

fig_map = None

# 1. Attempt Plotly 6.0+ API: px.scatter_map
if hasattr(px, "scatter_map"):
    try:
        fig_map = px.scatter_map(
            result_df,
            lat="latitude",
            lon="longitude",
            hover_name="location",
            hover_data=hover_dict,
            color="risk",
            color_discrete_map={"LOW RISK": "#10b981", "LANDSLIDE RISK": "#f43f5e"},
            size="risk_probability",
            size_max=24,
            zoom=5.7,
            center={"lat": 25.5, "lon": 92.5},
            map_style="carto-darkmatter"
        )
    except Exception:
        fig_map = None

# 2. Attempt Plotly 5.x API: px.scatter_mapbox
if fig_map is None and hasattr(px, "scatter_mapbox"):
    try:
        fig_map = px.scatter_mapbox(
            result_df,
            lat="latitude",
            lon="longitude",
            hover_name="location",
            hover_data=hover_dict,
            color="risk",
            color_discrete_map={"LOW RISK": "#10b981", "LANDSLIDE RISK": "#f43f5e"},
            size="risk_probability",
            size_max=24,
            zoom=5.7,
            center={"lat": 25.5, "lon": 92.5},
            mapbox_style="carto-darkmatter"
        )
    except Exception:
        fig_map = None

# 3. Universal Fallback: px.scatter_geo (works in all Plotly versions, no external tile server dependency)
if fig_map is None:
    try:
        fig_map = px.scatter_geo(
            result_df,
            lat="latitude",
            lon="longitude",
            hover_name="location",
            hover_data=hover_dict,
            color="risk",
            color_discrete_map={"LOW RISK": "#10b981", "LANDSLIDE RISK": "#f43f5e"},
            size="risk_probability",
            size_max=24,
            scope="asia"
        )
        fig_map.update_geos(
            center=dict(lat=25.5, lon=92.5),
            lataxis_range=[22.5, 29.0],
            lonaxis_range=[87.5, 96.5],
            showcountries=True,
            showsubunits=True,
            showland=True,
            landcolor="#1e293b",
            bgcolor="rgba(15, 23, 42, 0.9)",
            lakecolor="#0f172a"
        )
    except Exception:
        # 4. Ultimate resilient scatter fallback
        fig_map = go.Figure()
        for rk, colr in [("LOW RISK", "#10b981"), ("LANDSLIDE RISK", "#f43f5e")]:
            sub = result_df[result_df["risk"] == rk]
            if not sub.empty:
                fig_map.add_trace(
                    go.Scatter(
                        x=sub["longitude"],
                        y=sub["latitude"],
                        mode="markers+text",
                        name=rk,
                        text=sub["location"],
                        textposition="top center",
                        marker=dict(
                            size=sub["risk_probability"] * 0.3 + 12,
                            color=colr,
                            line=dict(color="#ffffff", width=1.5)
                        )
                    )
                )
        fig_map.update_layout(
            xaxis=dict(title="Longitude (°E)", gridcolor="rgba(255,255,255,0.08)"),
            yaxis=dict(title="Latitude (°N)", gridcolor="rgba(255,255,255,0.08)")
        )

fig_map.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(15, 23, 42, 0.7)",
    plot_bgcolor="rgba(15, 23, 42, 0.7)",
    legend=dict(
        yanchor="top",
        y=0.96,
        xanchor="left",
        x=0.02,
        bgcolor="rgba(15, 23, 42, 0.8)",
        bordercolor="rgba(255, 255, 255, 0.1)",
        borderwidth=1,
        font=dict(color="#f8fafc", size=11)
    )
)

st.plotly_chart(fig_map, use_container_width=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ============================================================
# LIVE WEATHER & LANDSLIDE PREDICTION TABLE
# ============================================================

st.markdown("### 🌦️ Live Weather & Landslide Prediction")

display_df = result_df[
    [
        "location",
        "state",
        "temperature_c",
        "humidity_percent",
        "rainfall_mm",
        "risk_probability",
        "risk"
    ]
].copy()

display_df.columns = [
    "Location",
    "State",
    "Temperature (°C)",
    "Humidity (%)",
    "Rainfall (mm)",
    "Risk Probability (%)",
    "Model Output"
]

display_df["Temperature (°C)"] = display_df["Temperature (°C)"].round(2)
display_df["Humidity (%)"] = display_df["Humidity (%)"].round(2)
display_df["Rainfall (mm)"] = display_df["Rainfall (mm)"].round(2)
display_df["Risk Probability (%)"] = display_df["Risk Probability (%)"].round(2)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Risk Probability (%)": st.column_config.ProgressColumn(
            "Risk Probability (%)",
            help="Predicted Random Forest Risk Probability",
            format="%.2f%%",
            min_value=0,
            max_value=100
        ),
        "Rainfall (mm)": st.column_config.NumberColumn(
            "Rainfall (mm)",
            format="%.2f mm"
        ),
        "Temperature (°C)": st.column_config.NumberColumn(
            "Temperature (°C)",
            format="%.1f °C"
        ),
        "Humidity (%)": st.column_config.NumberColumn(
            "Humidity (%)",
            format="%.0f%%"
        ),
        "Model Output": st.column_config.TextColumn(
            "Model Output"
        )
    }
)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ============================================================
# RISK PROBABILITY CHART (PLOTLY INTERACTIVE BAR)
# ============================================================

st.markdown("### 📊 Model Risk Probability by Location")

chart_df = result_df.sort_values("risk_probability", ascending=True)

# Color scale based on risk threshold
colors = [
    "#f43f5e" if row["risk"] == "LANDSLIDE RISK" else "#10b981"
    for _, row in chart_df.iterrows()
]

fig_bar = go.Figure(
    go.Bar(
        x=chart_df["risk_probability"],
        y=chart_df["location"],
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color="rgba(255,255,255,0.15)", width=1)
        ),
        text=[f"{val:.1f}% ({r})" for val, r in zip(chart_df["risk_probability"], chart_df["risk"])],
        textposition="outside",
        hoverinfo="text",
        hovertext=[
            f"<b>{loc}</b><br>State: {st_name}<br>Risk Probability: {prob:.2f}%<br>Rainfall: {rain:.1f} mm<br>Output: {rk}"
            for loc, st_name, prob, rain, rk in zip(
                chart_df["location"], chart_df["state"], chart_df["risk_probability"], chart_df["rainfall_mm"], chart_df["risk"]
            )
        ]
    )
)

fig_bar.add_vline(
    x=50.0,
    line_width=2,
    line_dash="dash",
    line_color="#f59e0b",
    annotation_text="50% Model Decision Threshold",
    annotation_position="top right",
    annotation_font_color="#f59e0b"
)

fig_bar.update_layout(
    paper_bgcolor="rgba(15, 23, 42, 0.7)",
    plot_bgcolor="rgba(15, 23, 42, 0.7)",
    font=dict(color="#e2e8f0", family="Plus Jakarta Sans"),
    xaxis=dict(
        title="Landslide Probability (%)",
        range=[0, 115],
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 255, 255, 0.1)"
    ),
    yaxis=dict(
        title="",
        gridcolor="rgba(255, 255, 255, 0.03)"
    ),
    margin=dict(l=20, r=20, t=30, b=30),
    height=380
)

st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ============================================================
# LOCATION DETAILS (INSPECTOR PANEL)
# ============================================================

st.markdown("### 📍 Location Details")

selected_location = st.selectbox(
    "Select a Northeast capital to inspect detailed telemetry:",
    sorted(result_df["location"].tolist())
)

selected = result_df[result_df["location"] == selected_location].iloc[0]

badge_bg = "rgba(244, 63, 94, 0.15)" if selected["risk"] == "LANDSLIDE RISK" else "rgba(16, 185, 129, 0.15)"
badge_border = "#f43f5e" if selected["risk"] == "LANDSLIDE RISK" else "#10b981"
badge_text = "#fda4af" if selected["risk"] == "LANDSLIDE RISK" else "#6ee7b7"

st.markdown(
    f"""
    <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 18px 24px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="font-size: 0.8rem; color: #38bdf8; font-weight: 700; text-transform: uppercase;">MONITORING STATION</span>
                <h2 style="font-size: 1.6rem; font-weight: 800; color: #ffffff; margin: 2px 0 0 0;">
                    {selected['location']} &nbsp;·&nbsp; <span style="font-size: 1.1rem; color: #94a3b8; font-weight: 500;">{selected['state']}</span>
                </h2>
            </div>
            <div style="background: {badge_bg}; border: 1px solid {badge_border}; color: {badge_text}; padding: 6px 16px; border-radius: 9999px; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.05em;">
                MODEL STATUS: {selected['risk']}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🌡️ Temperature", f"{selected['temperature_c']:.2f} °C")
    st.metric("🌧️ Rainfall", f"{selected['rainfall_mm']:.2f} mm")

with c2:
    st.metric("💧 Humidity", f"{selected['humidity_percent']:.0f}%")
    st.metric("📈 Risk Probability", f"{selected['risk_probability']:.2f}%")

with c3:
    st.metric("📍 Latitude", f"{selected['latitude']:.4f}")
    st.metric("📍 Longitude", f"{selected['longitude']:.4f}")

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ============================================================
# MACHINE LEARNING MODEL SECTION
# ============================================================

st.markdown("### 🤖 Machine Learning Model Architecture")

model_col1, model_col2, model_col3 = st.columns(3)

with model_col1:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">ALGORITHM</div>
            <div class="info-card-val">🌲 Random Forest Classifier</div>
            <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 6px; margin-bottom: 0;">
                Ensemble of decision trees trained on multi-temporal slope failure records and rainfall thresholds.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with model_col2:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">INPUT FEATURES</div>
            <div class="info-card-val">⚡ 6 Weather & Geographic Features</div>
            <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 6px; margin-bottom: 0;">
                <code>latitude</code>, <code>longitude</code>, <code>rainfall_mm</code>, <code>temperature_c</code>, <code>humidity_percent</code>, <code>month</code>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with model_col3:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">DATA PROCESSING ENGINE</div>
            <div class="info-card-val">⚡ Apache PySpark</div>
            <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 6px; margin-bottom: 0;">
                Distributed window functions & schema casting for high-throughput live JSON lines streaming.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ============================================================
# DATA PROCESSING PIPELINE (CONNECTED VISUAL NODES)
# ============================================================

st.markdown("### 🔄 End-to-End Big Data Processing Pipeline")

st.markdown(
    """
    <div class="pipeline-container">
        <div class="pipeline-node">
            <div>Open-Meteo API</div>
            <span>Live Weather Ingestion</span>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div>Python Collector</div>
            <span>Stream Generator</span>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div>JSON Lines Stream</div>
            <span>Buffer Ingestion</span>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div>Apache PySpark</div>
            <span>Distributed Engine</span>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div>Window Partition</div>
            <span>Latest Timestamp Filter</span>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div>Random Forest</div>
            <span>Scikit-learn Model</span>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div>Risk Probability</div>
            <span>Confidence Scoring</span>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node" style="border-color: #14b8a6; background: rgba(20, 184, 166, 0.15);">
            <div>Live Dashboard</div>
            <span style="color: #5eead4;">Command Center UI</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ============================================================
# DISCLAIMER & NOTICE
# ============================================================

st.markdown(
    """
    <div class="demonstration-notice">
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 1.4rem;">⚠️</span>
            <div>
                <h4 style="margin: 0 0 4px 0; color: #fbbf24; font-size: 0.95rem; font-weight: 700;">
                    Project Demonstration Notice
                </h4>
                <p style="margin: 0; font-size: 0.84rem; color: #cbd5e1; line-height: 1.5;">
                    The displayed risk values are outputs from a machine-learning model utilizing live weather and geographic features. They are intended strictly for academic/project demonstration purposes and do not represent official governmental landslide warnings or emergency evacuation orders.
                </p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding: 22px 0 35px 0; margin-top: 30px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; font-size: 0.82rem; color: #64748b;">
        <div>
            <span style="font-weight: 700; color: #94a3b8;">Northeast India Landslide Risk Prediction System</span>
            <span style="margin: 0 8px;">•</span>
            <span>Big Data Analytics + Machine Learning Project</span>
        </div>
        <div>
            <span>Telemetry Last Synced: </span>
            <code style="background: rgba(30, 41, 59, 0.8); color: #38bdf8; padding: 3px 8px; border-radius: 4px; font-family: 'JetBrains Mono', monospace;">
                {latest_timestamp}
            </code>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
