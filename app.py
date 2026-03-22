import pandas as pd
import streamlit as st

st.set_page_config(page_title="Supplier Risk System", layout="wide")

# Title
st.title("Supplier Evaluation & Risk Scoring System")
st.markdown("### Real-time Supplier Risk Analysis Dashboard")

# Load data
df = pd.read_csv("suppliers.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Model Configuration")

delivery_weight = st.sidebar.slider("Delivery Weight", 0.0, 1.0, 0.3)
quality_weight = st.sidebar.slider("Quality Weight", 0.0, 1.0, 0.3)
cost_weight = st.sidebar.slider("Cost Weight", 0.0, 1.0, 0.2)
compliance_weight = st.sidebar.slider("Compliance Weight", 0.0, 1.0, 0.2)

if round(delivery_weight + quality_weight + cost_weight + compliance_weight, 2) != 1.0:
    st.sidebar.error("⚠️ Total weight must equal 1.0")

# ---------------- KPI CALCULATION ----------------
df["DeliveryScore"] = df["OnTimeDelivery"] / 100
df["QualityScore"] = 1 - (df["DefectRate"] / 100)
df["CostScore"] = 1 - (df["CostVariance"] / 100)
df["ComplianceScoreNorm"] = df["ComplianceScore"] / 100

df["RiskScore"] = (
    delivery_weight * df["DeliveryScore"] +
    quality_weight * df["QualityScore"] +
    cost_weight * df["CostScore"] +
    compliance_weight * df["ComplianceScoreNorm"]
)

# ---------------- CLASSIFICATION ----------------
def classify(score):
    if score >= 0.8:
        return "Low Risk"
    elif score >= 0.6:
        return "Medium Risk"
    else:
        return "High Risk"

df["RiskCategory"] = df["RiskScore"].apply(classify)

# Sort
df = df.sort_values(by="RiskScore")

# ---------------- KPI CARDS ----------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Suppliers", len(df))
col2.metric("High Risk", (df["RiskCategory"] == "High Risk").sum())
col3.metric("Medium Risk", (df["RiskCategory"] == "Medium Risk").sum())
col4.metric("Low Risk", (df["RiskCategory"] == "Low Risk").sum())

# ---------------- FILTER ----------------
st.subheader("🔍 Filter View")
option = st.selectbox("Select Supplier Category", ["All", "High Risk", "Medium Risk", "Low Risk"])

if option != "All":
    filtered_df = df[df["RiskCategory"] == option]
else:
    filtered_df = df

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Supplier Performance Table")
    st.dataframe(filtered_df, use_container_width=True)

with col2:
    st.subheader("📊 Risk Distribution")
    st.bar_chart(filtered_df["RiskCategory"].value_counts())

# ---------------- INSIGHTS ----------------
st.subheader("🚨 Critical Insights")

worst = df.iloc[0]
best = df.iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.error(f"Worst Supplier: {worst['Supplier']} (Score: {round(worst['RiskScore'],2)})")

with col2:
    st.success(f"Best Supplier: {best['Supplier']} (Score: {round(best['RiskScore'],2)})")

# ---------------- KPI TRENDS ----------------
st.subheader("📈 KPI Trends Across Suppliers")
st.line_chart(df[["DeliveryScore", "QualityScore", "CostScore"]])

# ---------------- ALERT SYSTEM ----------------
high_risk_count = (df["RiskCategory"] == "High Risk").sum()

if high_risk_count > 0:
    st.error(f"⚠️ ALERT: {high_risk_count} High Risk Suppliers detected!")
else:
    st.success("✅ No High Risk Suppliers")

# ---------------- DOWNLOAD ----------------
st.subheader("⬇️ Export Data")
st.download_button(
    "Download Full Report",
    df.to_csv(index=False),
    "supplier_report.csv"
)