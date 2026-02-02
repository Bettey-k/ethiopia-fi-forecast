📊 Ethiopia Financial Inclusion Forecasting (Week 10 – KAIM)
Project Overview

This project analyzes and forecasts financial inclusion in Ethiopia, focusing on two core dimensions:

Access: Account ownership (% of adults with an account at a financial institution or mobile money provider)

Usage: Digital payment adoption (% of adults making or receiving digital payments)

Given sparse Global Findex-style survey data, the project combines:

data enrichment

exploratory analysis

event impact modeling

scenario-based forecasting

an interactive Streamlit dashboard

The goal is to support policy makers, investors, and development partners in understanding historical dynamics and plausible future trajectories of financial inclusion in Ethiopia’s rapidly evolving mobile money ecosystem.

ethiopia-fi-forecast/
│
├── data/
│   ├── raw/                  # Original provided datasets
│   └── processed/            # Enriched data and forecast outputs
│
├── notebooks/
│   ├── task_1_data_enrichment.ipynb
│   ├── task_2_eda.ipynb
│   ├── task_3_event_impact_modeling.ipynb
│   └── task_4_forecasting.ipynb
│
├── dashboard/
│   └── app.py                # Streamlit dashboard (Task 5)
│
├── tests/
│   └── test_data_loading.py
│
├── data_enrichment_log.md
├── requirements.txt
└── README.md
Task 1: Data Exploration and Enrichment
Objectives

Understand the unified schema (observations, events, targets)

Review reference codes and impact link structure

Enrich the dataset with additional indicators and event relationships

Key Outputs

Cleaned and enriched dataset:
data/processed/ethiopia_fi_enriched.csv

Full documentation of additions and corrections in:
data_enrichment_log.md

Key Notes

Events are stored without pillar assignment to avoid misclassification

Indicator mapping is handled through the impact_links table

All new records include source, confidence, collection date, and notes

Task 2: Exploratory Data Analysis (EDA)
What Was Analyzed

Indicator coverage and temporal gaps

Trends in account ownership and digital payment usage

Divergence between rapid mobile money expansion and slower access growth

Visual overlay of major events on indicator trends

Key Findings

Account ownership growth slowed significantly between 2021–2024

Mobile money adoption expanded rapidly but did not translate directly into ownership

Data sparsity limits fine-grained causal inference

All EDA is contained in task_2_eda.ipynb with labeled visualizations and commentary.

Task 3: Event Impact Modeling
Methodology

Events (e.g., Telebirr launch, market entry) are linked to indicators using the impact_links table

Each link specifies:

impact direction

relative magnitude

lag in months

evidence basis

Historical Validation (Code-Based)

Explicit historical validation is included in the notebook by comparing:

Observed outcomes after the Telebirr launch (2021–2024)

Modeled expectations from the event impact assumptions

This validation confirms:

The modeled direction of impact aligns with observed trends

Usage responds more strongly than access, consistent with real-world dynamics

Model Assumptions (Documented in Notebook)

Event impacts are gradual, not instantaneous

Effects from multiple events are additive

Usage indicators are more elastic than access indicators

Task 4: Forecasting Access and Usage (2025–2027)
Forecasting Approach

Baseline trend modeled using simple linear regression on time

Scenario-based forecasting applied via multiplicative growth factors:

Pessimistic

Base

Optimistic

This approach prioritizes interpretability and robustness over overfitting, given sparse historical data.

Validation and Sanity Checks

Back-testing compares modeled vs observed historical values

Visual validation plots are included in the notebook

Forecasts are interpreted as scenario guidance, not precise predictions

Data Limitations (Explicitly Stated)

Very limited survey observations

Proxy indicators for usage

Partial reliance on expert judgment and comparable-country evidence

Forecast outputs are saved to:

data/processed/forecast_results.csv
ask 5: Interactive Dashboard

An interactive Streamlit dashboard was developed to allow stakeholders to:

View current inclusion metrics

Explore trends interactively

Compare scenario-based forecasts

Assess progress toward inclusion targets

Running the Dashboard Locally
pip install -r requirements.txt
streamlit run dashboard/app.py


The dashboard is intentionally lightweight and transparent, designed for decision support rather than black-box prediction.

Key Insights and Business Implications

Mobile money expansion alone is insufficient to drive formal account ownership

Policy focus should shift from registration counts to active usage

Upcoming regulatory and infrastructure events could materially alter future inclusion trajectories

Scenario analysis highlights trade-offs and uncertainty rather than single-point predictions

Conclusion

This project demonstrates how data enrichment, transparent assumptions, historical validation, and scenario-based forecasting can produce credible insights even in data-constrained environments. The framework is well-suited for strategic planning and can be refined as richer data becomes available.

Author

Betelhem Kibret Getu
KAIM – Week 10 Project
Financial Inclusion & Data Analytics