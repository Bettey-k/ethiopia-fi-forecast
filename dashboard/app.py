import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    layout="wide"
)

st.title("📊 Ethiopia Financial Inclusion Dashboard")

# -----------------------------
# Resolve paths safely
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "ethiopia_fi_enriched.csv"

# -----------------------------
# Load data (with visible errors)
# -----------------------------
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    data = load_data(DATA_PATH)
    st.success("✅ Data loaded successfully")
except Exception as e:
    st.error("❌ Failed to load data")
    st.exception(e)
    st.stop()

# Prepare observations
obs = data[data["record_type"] == "observation"].copy()
obs["year"] = pd.to_datetime(obs["observation_date"]).dt.year

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["Overview", "Trends", "Forecasts"]
)

# ======================================================
# OVERVIEW PAGE
# ======================================================
if page == "Overview":
    st.header("📌 Overview")

    col1, col2 = st.columns(2)

    latest_access = (
        obs[obs["indicator_code"] == "ACC_OWNERSHIP"]
        .sort_values("year")
        .iloc[-1]
    )

    latest_mm = (
        obs[obs["indicator_code"] == "ACC_MM_ACCOUNT"]
        .sort_values("year")
        .iloc[-1]
    )

    col1.metric(
        "Account Ownership (%)",
        f"{latest_access.value_numeric:.1f}"
    )

    col2.metric(
        "Mobile Money Accounts (%)",
        f"{latest_mm.value_numeric:.1f}"
    )

    st.markdown(
        """
        **Insight:**  
        Mobile money adoption has grown faster than formal account ownership,
        highlighting a divergence between Access and Usage.
        """
    )

# ======================================================
# TRENDS PAGE
# ======================================================
elif page == "Trends":
    st.header("📈 Trends")

    indicator = st.selectbox(
        "Select Indicator",
        obs["indicator"].dropna().unique()
    )

    subset = obs[obs["indicator"] == indicator]

    fig = px.line(
        subset,
        x="year",
        y="value_numeric",
        markers=True,
        title=f"{indicator} Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "Download Data",
        subset.to_csv(index=False),
        file_name="trend_data.csv"
    )

# ======================================================
# FORECASTS PAGE
# ======================================================
elif page == "Forecasts":
    st.header("🔮 Forecasts & Scenarios")

    FORECAST_PATH = BASE_DIR / "data" / "processed" / "forecast_results.csv"

    try:
        forecast_df = pd.read_csv(FORECAST_PATH)
        st.success("✅ Forecast data loaded")
    except Exception as e:
        st.error("❌ Forecast file not found")
        st.exception(e)
        st.stop()

    # Scenario selector
    scenario = st.radio(
        "Select Scenario",
        forecast_df["scenario"].unique(),
        horizontal=True
    )

    f = forecast_df[forecast_df["scenario"] == scenario]

    # Usage forecast
    fig_usage = px.line(
        f,
        x="year",
        y="usage_forecast",
        markers=True,
        title=f"Digital Payment Usage Forecast ({scenario.capitalize()})"
    )

    st.plotly_chart(fig_usage, use_container_width=True)

    # Access forecast
    fig_access = px.line(
        f,
        x="year",
        y="access_forecast",
        markers=True,
        title=f"Account Ownership Forecast ({scenario.capitalize()})"
    )

    st.plotly_chart(fig_access, use_container_width=True)

    st.markdown(
        """
        **Interpretation:**  
        Forecasts are scenario-based due to limited historical survey data.
        Usage grows faster than access under all scenarios, reflecting
        Ethiopia’s mobile-money–driven digital finance expansion.
        """
    )

    st.download_button(
        "Download Forecast Data",
        f.to_csv(index=False),
        file_name="forecast_data.csv"
    )
