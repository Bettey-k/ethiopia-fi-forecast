import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    layout="wide"
)

st.title("📊 Ethiopia Financial Inclusion Dashboard")

# --------------------------------------------------
# Resolve paths safely
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "ethiopia_fi_enriched.csv"
FORECAST_PATH = BASE_DIR / "data" / "processed" / "forecast_results.csv"

# --------------------------------------------------
# Load data with visible error handling
# --------------------------------------------------
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    data = load_data(DATA_PATH)
    st.success("✅ Data loaded successfully")
except Exception as e:
    st.error("❌ Failed to load main dataset")
    st.exception(e)
    st.stop()

# Prepare observations
obs = data[data["record_type"] == "observation"].copy()
obs["year"] = pd.to_datetime(obs["observation_date"]).dt.year

# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["Overview", "Trends", "Forecasts", "Inclusion Projections"]
)

# ==================================================
# OVERVIEW PAGE
# ==================================================
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
        highlighting a divergence between **Access** and **Usage** in Ethiopia’s
        digital financial ecosystem.
        """
    )

# ==================================================
# TRENDS PAGE
# ==================================================
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

# ==================================================
# FORECASTS PAGE
# ==================================================
elif page == "Forecasts":
    st.header("🔮 Forecasts & Scenarios")

    try:
        forecast_df = pd.read_csv(FORECAST_PATH)
        st.success("✅ Forecast data loaded")
    except Exception as e:
        st.error("❌ Forecast data not found")
        st.exception(e)
        st.stop()

    scenario = st.radio(
        "Select Scenario",
        forecast_df["scenario"].unique(),
        horizontal=True
    )

    f = forecast_df[forecast_df["scenario"] == scenario]

    fig_usage = px.line(
        f,
        x="year",
        y="usage_forecast",
        markers=True,
        title=f"Digital Payment Usage Forecast ({scenario.capitalize()})"
    )

    st.plotly_chart(fig_usage, use_container_width=True)

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
        Across all scenarios, usage grows faster than access, reflecting
        Ethiopia’s mobile-money–driven inclusion model and persistent
        structural barriers to full account ownership.
        """
    )

    st.download_button(
        "Download Forecast Data",
        f.to_csv(index=False),
        file_name="forecast_data.csv"
    )

# ==================================================
# INCLUSION PROJECTIONS PAGE
# ==================================================
elif page == "Inclusion Projections":
    st.header("🎯 Inclusion Projections")

    TARGET = 60  # Consortium target (%)

    try:
        forecast_df = pd.read_csv(FORECAST_PATH)
    except Exception as e:
        st.error("❌ Forecast data not found")
        st.exception(e)
        st.stop()

    scenario = st.radio(
        "Select Scenario",
        forecast_df["scenario"].unique(),
        horizontal=True
    )

    f = forecast_df[forecast_df["scenario"] == scenario]

    fig = px.line(
        f,
        x="year",
        y="access_forecast",
        markers=True,
        title="Projected Account Ownership vs 60% Target"
    )

    fig.add_hline(
        y=TARGET,
        line_dash="dash",
        annotation_text="60% Target"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        **Consortium Question:**  
        Will Ethiopia reach 60% account ownership by 2027?

        **Answer:**  
        Under the selected scenario, Ethiopia does **not** reach the 60% target
        by 2027, highlighting the need for stronger policy, infrastructure,
        and inclusion-focused interventions.
        """
    )
