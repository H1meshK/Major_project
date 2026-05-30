import pandas as pd
import streamlit as st
from utils import load_supplier_data, calculate_kpi_scores

st.set_page_config(page_title="Supplier Risk System", layout="wide")

st.title("JMP Jalandhar - Supplier Risk & Performance Analytics System")
with st.expander("About this Dashboard", expanded=False):
    st.info("""
    This dashboard provides procurement managers with a centralized platform
    for evaluating supplier reliability, operational risks, quality performance,
    cost efficiency and compliance metrics.

    The system combines:
    * Weighted Risk Scoring Analysis
    * Data Envelopment Analysis (DEA)
    * Supplier Benchmarking
    * Procurement Risk Monitoring
    """)    
st.markdown("### Real-time Supplier Risk Analysis Dashboard")

# Load data
df = load_supplier_data()
df = calculate_kpi_scores(df)

with st.expander("Business Context", expanded=False):
    st.markdown("""
    JMP Jalandhar relies on multiple suppliers for maintaining manufacturing
    continuity and operational excellence.

    This system assists procurement teams in:
    * Monitoring supplier performance
    * Identifying high-risk vendors
    * Benchmarking supplier efficiency
    * Supporting supplier selection decisions
    * Improving supply chain resilience
    """)
    
st.markdown("""
Welcome to the **Supplier Evaluation & Risk Scoring System**. This dashboard provides 
comprehensive analysis of supplier performance using two complementary methods:

1. **Weighted Risk Scoring Method** - Customizable multi-factor risk evaluation
2. **Data Envelopment Analysis (DEA)** - Efficiency frontier analysis

Select a page from the sidebar to get started!
""")


st.subheader("Available Analysis Modules")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    ### Weighted Risk Scoring

    Evaluate suppliers using customizable KPI weights.

    ✔ Risk Categorization

    ✔ Supplier Ranking

    ✔ Performance Monitoring
    """)

with col2:
    st.info("""
    ### DEA Efficiency Analysis

    Benchmark suppliers using efficiency frontier analysis.

    ✔ Efficiency Scores

    ✔ Benchmarking

    ✔ Improvement Opportunities
    """)

    
# ============ DATASET OVERVIEW ============
st.subheader("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Vendors",
    len(df)
)

col2.metric(
    "Avg Delivery",
    f"{df['OnTimeDelivery'].mean():.1f}%"
)

col3.metric(
    "Avg Compliance",
    f"{df['ComplianceScore'].mean():.1f}%"
)

col4.metric(
    "Avg Quality",
    f"{100-df['DefectRate'].mean():.1f}%"
)

# ============ PERFORMANCE SUMMARY ============
st.subheader("Performance Summary")

col1, col2 = st.columns(2)

with col1:
    st.write("**On-Time Delivery Distribution**")
    delivery_hist = df["OnTimeDelivery"].value_counts().sort_index()
    st.bar_chart(delivery_hist)

with col2:
    st.write("**Defect Rate Distribution**")
    defect_hist = df["DefectRate"].value_counts().sort_index()
    st.bar_chart(defect_hist)

# ============ SUPPLIER TABLE ============
st.subheader("Supplier Performance Data")

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.write("Raw supplier metrics from suppliers.csv")

with col2:
    show_summary = st.checkbox("Show Summary Only", value=False)

with col3:
    if st.button("Show All Columns"):
        show_summary = False

if show_summary:
    display_cols = ["Supplier", "OnTimeDelivery", "DefectRate", "CostVariance", "ComplianceScore"]
else:
    display_cols = ["Supplier", "OnTimeDelivery", "DefectRate", "CostVariance", "ComplianceScore"]

display_df = df[display_cols].copy()
st.dataframe(display_df, use_container_width=True)

# ============ KPI BREAKDOWN ============
st.subheader("Calculated KPI Scores")

st.write("""
The system calculates normalized KPI scores for each supplier:
- **Delivery Score** = OnTimeDelivery / 100
- **Quality Score** = 1 - (DefectRate / 100)
- **Cost Score** = 1 - (CostVariance / 100)
- **Compliance Score** = ComplianceScore / 100
""")

kpi_df = df[["Supplier", "DeliveryScore", "QualityScore", "CostScore", "ComplianceScoreNorm"]].copy()
kpi_df = kpi_df.round(3)
st.dataframe(kpi_df, use_container_width=True)

st.subheader("Executive Summary")

best_delivery = df["OnTimeDelivery"].max()
avg_defect = df["DefectRate"].mean()

st.success(
    f"""
    Current supplier network consists of {len(df)} vendors.

    Average delivery performance is {df['OnTimeDelivery'].mean():.1f}%,
    while average defect rate remains {avg_defect:.1f}%.

    This dashboard enables proactive identification of supplier risks
    and efficiency improvement opportunities.
    """
)

# ============ KEY STATISTICS ============
st.subheader("Key Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("**Delivery Score**")
    st.metric("Mean", f"{df['DeliveryScore'].mean():.3f}")
    st.metric("Range", f"{df['DeliveryScore'].min():.3f} - {df['DeliveryScore'].max():.3f}")

with col2:
    st.write("**Quality Score**")
    st.metric("Mean", f"{df['QualityScore'].mean():.3f}")
    st.metric("Range", f"{df['QualityScore'].min():.3f} - {df['QualityScore'].max():.3f}")

with col3:
    st.write("**Cost Score**")
    st.metric("Mean", f"{df['CostScore'].mean():.3f}")
    st.metric("Range", f"{df['CostScore'].min():.3f} - {df['CostScore'].max():.3f}")

with col4:
    st.write("**Compliance Score**")
    st.metric("Mean", f"{df['ComplianceScoreNorm'].mean():.3f}")
    st.metric("Range", f"{df['ComplianceScoreNorm'].min():.3f} - {df['ComplianceScoreNorm'].max():.3f}")

# ============ INSTRUCTIONS ============
st.subheader("Getting Started")

st.markdown("""
### Choose your analysis method:

**Weighted Risk Scoring Method**
- Customize weights for each KPI factor
- Get weighted risk scores and categorization
- Real-time interactive dashboards
- Filter suppliers by risk level

Navigate to **Weighted Method** in the sidebar

**Data Envelopment Analysis (DEA)**
- Identify efficiency frontiers
- Benchmark suppliers against each other
- Input-output optimization analysis
- Detailed efficiency rankings

Navigate to **DEA Analysis** in the sidebar
""")

# ============ DOWNLOAD OPTION ============
st.subheader("Export Raw Data")

st.download_button(
    label="Download All Supplier Data (CSV)",
    data=df.to_csv(index=False),
    file_name="supplier_data_all.csv",
    mime="text/csv"
)
