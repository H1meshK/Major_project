import pandas as pd
import streamlit as st
from utils import load_supplier_data, calculate_kpi_scores, classify_risk

st.set_page_config(page_title="Weighted Method", layout="wide")

st.title("Weighted Risk Scoring Method")
st.markdown("### Customizable multi-factor supplier risk evaluation")

# Load data
df = load_supplier_data()
df = calculate_kpi_scores(df)

# ============ CONFIGURATION ============
st.sidebar.header("Model Configuration")

delivery_weight = st.sidebar.slider("Delivery Weight", 0.0, 1.0, 0.3)
quality_weight = st.sidebar.slider("Quality Weight", 0.0, 1.0, 0.3)
cost_weight = st.sidebar.slider("Cost Weight", 0.0, 1.0, 0.2)
compliance_weight = st.sidebar.slider("Compliance Weight", 0.0, 1.0, 0.2)

total_weight = round(delivery_weight + quality_weight + cost_weight + compliance_weight, 2)

if total_weight != 1.0:
    st.sidebar.error(f"Total weight must equal 1.0 (current: {total_weight})")
else:
    st.sidebar.success(f"Weights valid (total: {total_weight})")

# ============ CALCULATE WEIGHTED RISK SCORE ============
df["RiskScore"] = (
    delivery_weight * df["DeliveryScore"] +
    quality_weight * df["QualityScore"] +
    cost_weight * df["CostScore"] +
    compliance_weight * df["ComplianceScoreNorm"]
)

df["RiskCategory"] = df["RiskScore"].apply(classify_risk)
df = df.sort_values(by="RiskScore", ascending=False)

# ============ KPI METRICS ============
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Suppliers", len(df))
col2.metric("Low Risk", (df["RiskCategory"] == "Low Risk").sum())
col3.metric("Medium Risk", (df["RiskCategory"] == "Medium Risk").sum())
col4.metric("High Risk", (df["RiskCategory"] == "High Risk").sum())

# ============ WEIGHT BREAKDOWN ============
st.subheader("Weight Distribution")
weight_data = pd.DataFrame({
    "Factor": ["Delivery", "Quality", "Cost", "Compliance"],
    "Weight": [delivery_weight, quality_weight, cost_weight, compliance_weight]
})
st.bar_chart(weight_data.set_index("Factor"))

# ============ FILTER ============
st.subheader("Filter & View")
filter_option = st.selectbox(
    "Select Supplier Category",
    ["All", "Low Risk", "Medium Risk", "High Risk"]
)

if filter_option != "All":
    filtered_df = df[df["RiskCategory"] == filter_option].copy()
else:
    filtered_df = df.copy()

# ============ MAIN DISPLAY ============
col1, col2 = st.columns(2)

with col1:
    st.subheader("Supplier Scores Table")
    display_cols = ["Supplier", "RiskScore", "RiskCategory"]
    display_df = filtered_df[display_cols].copy()
    display_df["RiskScore"] = display_df["RiskScore"].round(3)
    st.dataframe(display_df, use_container_width=True)

with col2:
    st.subheader("Risk Category Distribution")
    risk_counts = df["RiskCategory"].value_counts()
    st.bar_chart(risk_counts)

# ============ KPI COMPONENT BREAKDOWN ============
st.subheader("Individual KPI Scores")

col1, col2 = st.columns(2)

with col1:
    st.write("**Delivery Performance vs Compliance**")
    scatter_data = df[["Supplier", "DeliveryScore", "ComplianceScoreNorm"]].copy()
    scatter_data = scatter_data.rename(columns={"DeliveryScore": "Delivery", "ComplianceScoreNorm": "Compliance"})
    st.scatter_chart(scatter_data.set_index("Supplier"))

with col2:
    st.write("**Quality vs Cost Efficiency**")
    scatter_data2 = df[["Supplier", "QualityScore", "CostScore"]].copy()
    scatter_data2 = scatter_data2.rename(columns={"QualityScore": "Quality", "CostScore": "Cost"})
    st.scatter_chart(scatter_data2.set_index("Supplier"))

# ============ DETAILED TRENDS ============
st.subheader("KPI Trends")
st.line_chart(df.set_index("Supplier")[["DeliveryScore", "QualityScore", "CostScore"]])

# ============ CRITICAL INSIGHTS ============
st.subheader("Critical Insights")

best_idx = df["RiskScore"].idxmax()
worst_idx = df["RiskScore"].idxmin()

best = df.loc[best_idx]
worst = df.loc[worst_idx]

col1, col2 = st.columns(2)

with col1:
    st.success(f"Best Performer: **{best['Supplier']}**\nRisk Score: {round(best['RiskScore'], 3)}\nCategory: {best['RiskCategory']}")

with col2:
    st.error(f"Worst Performer: **{worst['Supplier']}**\nRisk Score: {round(worst['RiskScore'], 3)}\nCategory: {worst['RiskCategory']}")

# ============ ALERT SYSTEM ============
st.subheader("Alerts")

high_risk_count = (df["RiskCategory"] == "High Risk").sum()

if high_risk_count > 0:
    st.warning(f"{high_risk_count} supplier(s) classified as High Risk")
else:
    st.info("No high-risk suppliers detected")

# ============ EXPORT ============
st.subheader("Export Data")
st.download_button(
    label="Download Weighted Risk Report (CSV)",
    data=df.to_csv(index=False),
    file_name="weighted_risk_report.csv",
    mime="text/csv"
)
