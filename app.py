import pandas as pd
import streamlit as st
import plotly.express as px
from utils import load_supplier_data, calculate_kpi_scores

# ============ PAGE CONFIGURATION ============
st.set_page_config(page_title="Supplier Risk System", layout="wide")

# ============ GLOBAL CSS STYLING ============
st.markdown("""
    <style>
    /* Targets bordered containers to give them an opaque, modern background */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(240, 242, 246, 0.85);
        border: 1px solid #e0e0e0 !important;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    @media (prefers-color-scheme: dark) {
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: rgba(38, 39, 48, 0.85);
            border: 1px solid #444 !important;
        }
    }
    
    [data-testid="stMetricValue"] {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# ============ SIDEBAR & GLOBAL DATA LOADING ============
st.sidebar.title("Data Controls")
# 1. Place the uploader in the sidebar so it controls the whole app globally
uploaded_file = st.sidebar.file_uploader("📂 Upload Supplier Data (CSV)", type=["csv"])

@st.cache_data
def get_data(file):
    if file is not None:
        # If user uploaded a file, read it and replace the default data
        raw_df = pd.read_csv(file)
    else:
        # Otherwise, load the default local data
        raw_df = load_supplier_data()
        
    # Calculate KPIs on whichever data was loaded
    return calculate_kpi_scores(raw_df)

# 2. Initialize the global dataframe (this powers the entire dashboard)
df = get_data(uploaded_file)

# ============ HEADER ============
st.title("JMP Jalandhar - Supplier Risk & Performance Analytics System")
st.markdown("### Real-time Supplier Risk Analysis Dashboard")

with st.expander("About this Dashboard", expanded=False):
    st.info("""
This dashboard provides procurement managers and supply chain professionals with a centralized platform for evaluating supplier performance, operational reliability, procurement risks, quality consistency, cost efficiency, compliance adherence, lead time performance, order fulfillment capability, and supplier responsiveness.

The system has been developed to support data-driven supplier selection and performance monitoring within manufacturing environments such as JMP Jalandhar, where supplier performance directly impacts production continuity, inventory availability, product quality, and overall operational efficiency.

Key capabilities of the dashboard include:
• Weighted Risk Scoring Analysis for comprehensive supplier risk assessment
• Data Envelopment Analysis (DEA) for measuring relative supplier efficiency
• Supplier Benchmarking to compare suppliers against peers
• Procurement Risk Monitoring for early identification of suppliers
• Lead Time and Responsiveness Analysis
• Order Fulfillment Tracking
• Interactive Data Visualization and Reporting
• Exportable Reports for procurement reviews

The dashboard enables organizations to improve supplier selection processes, reduce supply chain disruptions, enhance procurement efficiency, and build a more resilient and reliable supplier network.
    """)    

# ============ BUSINESS CONTEXT ============
with st.container(border=True):
    with st.expander("Business Context", expanded=False):
        st.markdown("""
        JMP Jalandhar relies on multiple suppliers for maintaining manufacturing
        continuity and operational excellence.

        **This system assists procurement teams in:**
        • Monitoring supplier performance
        • Identifying high-risk vendors
        • Benchmarking supplier efficiency
        • Supporting supplier selection decisions
        • Improving supply chain resilience
        """)
        
    st.markdown("""
    Welcome to the **Supplier Evaluation & Risk Scoring System**. This dashboard provides 
    comprehensive analysis of supplier performance using two complementary methods:

    **1. Weighted Risk Scoring Method** - Customizable multi-factor risk evaluation
    **2. Data Envelopment Analysis (DEA)** - Efficiency frontier analysis

    > **Note:** Select a page from the sidebar to get started!
    """)

st.divider()

# ============ ANALYSIS MODULES ============
st.subheader("Available Analysis Modules")

col1, col2 = st.columns(2)
with col1:
    st.success("""
    ### Weighted Risk Scoring
    Evaluate suppliers using customizable KPI weights.
    • Risk Categorization
    • Supplier Ranking
    • Performance Monitoring
    """)
with col2:
    st.info("""
    ### DEA Efficiency Analysis
    Benchmark suppliers using efficiency frontier analysis.
    • Efficiency Scores
    • Benchmarking
    • Improvement Opportunities
    """)

st.divider()

# ============ EXECUTIVE SUMMARY ============
st.subheader("Executive Summary")
best_delivery = df["OnTimeDelivery"].max()
avg_defect = df["DefectRate"].mean()

st.success(
    f"""
    Current supplier network consists of **{len(df)}** vendors.

    Average delivery performance is **{df['OnTimeDelivery'].mean():.1f}%**,
    while average defect rate remains **{avg_defect:.1f}%**.

    This dashboard enables proactive identification of supplier risks
    and efficiency improvement opportunities.
    """
)

st.divider()

# ============ MAIN CONTENT TABS ============
# Added a 5th tab specifically for the newly uploaded data
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Dataset Overview & Visuals", 
    "Supplier Table", 
    "Calculated KPIs", 
    "Uploaded Data Insights",
    "Getting Started"
])

# --- TAB 1: OVERVIEW & VISUALS ---
with tab1:
    st.subheader("Dataset Overview")
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Vendors", len(df))
        col2.metric("Avg Delivery", f"{df['OnTimeDelivery'].mean():.1f}%")
        col3.metric("Avg Compliance", f"{df['ComplianceScore'].mean():.1f}%")
        col4.metric("Avg Quality", f"{100-df['DefectRate'].mean():.1f}%")

    st.subheader("Performance Summary")
    with st.container(border=True):
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("**On-Time Delivery Distribution**")
            fig_delivery = px.histogram(df, x="OnTimeDelivery", nbins=15, color_discrete_sequence=["#2ca02c"])
            fig_delivery.update_traces(marker_line_color='black', marker_line_width=0.8)
            fig_delivery.update_layout(margin=dict(l=20, r=20, t=20, b=20), xaxis_title="On-Time Delivery (%)", yaxis_title="Count")
            st.plotly_chart(fig_delivery, use_container_width=True)

        with chart_col2:
            st.markdown("**Defect Rate Distribution**")
            fig_defect = px.histogram(df, x="DefectRate", nbins=15, color_discrete_sequence=["#d62728"])
            fig_defect.update_traces(marker_line_color='black', marker_line_width=0.8)
            fig_defect.update_layout(margin=dict(l=20, r=20, t=20, b=20), xaxis_title="Defect Rate (%)", yaxis_title="Count")
            st.plotly_chart(fig_defect, use_container_width=True)

    st.subheader("Key Statistics")
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**Delivery Score**")
            st.metric("Mean", f"{df['DeliveryScore'].mean():.3f}")
            st.metric("Range", f"{df['DeliveryScore'].min():.3f} - {df['DeliveryScore'].max():.3f}")
        with col2:
            st.markdown("**Quality Score**")
            st.metric("Mean", f"{df['QualityScore'].mean():.3f}")
            st.metric("Range", f"{df['QualityScore'].min():.3f} - {df['QualityScore'].max():.3f}")
        with col3:
            st.markdown("**Cost Score**")
            st.metric("Mean", f"{df['CostScore'].mean():.3f}")
            st.metric("Range", f"{df['CostScore'].min():.3f} - {df['CostScore'].max():.3f}")
        with col4:
            st.markdown("**Compliance Score**")
            st.metric("Mean", f"{df['ComplianceScoreNorm'].mean():.3f}")
            st.metric("Range", f"{df['ComplianceScoreNorm'].min():.3f} - {df['ComplianceScoreNorm'].max():.3f}")

# --- TAB 2: SUPPLIER TABLE ---
with tab2:
    st.subheader("Supplier Performance Data")
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write("Raw supplier metrics view")
        with col2:
            show_summary = st.checkbox("Show Summary Only", value=True)
        with col3:
            if st.button("Show All Columns", use_container_width=True):
                show_summary = False

        if show_summary:
            display_cols = ["Supplier", "OnTimeDelivery", "DefectRate", "CostVariance", "ComplianceScore"]
        else:
            # Fixed this so it actually shows all columns when the button is clicked!
            display_cols = df.columns.tolist() 

        display_df = df[display_cols].copy()
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# --- TAB 3: KPI BREAKDOWN ---
with tab3:
    st.subheader("Calculated KPI Scores")
    with st.container(border=True):
        st.markdown("""
        **The system calculates normalized KPI scores for each supplier:**
        • **Delivery Score** = OnTimeDelivery / 100
        • **Quality Score** = 1 - (DefectRate / 100)
        • **Cost Score** = 1 - (CostVariance / 100)
        • **Compliance Score** = ComplianceScore / 100
        """)

        kpi_df = df[["Supplier", "DeliveryScore", "QualityScore", "CostScore", "ComplianceScoreNorm"]].copy()
        kpi_df = kpi_df.round(3)
        
        styled_kpi = kpi_df.style.background_gradient(cmap="RdYlGn", subset=["DeliveryScore", "QualityScore", "CostScore", "ComplianceScoreNorm"], vmin=0.0, vmax=1.0)
        st.dataframe(styled_kpi, use_container_width=True, hide_index=True)

# --- TAB 4: NEW DATA INSIGHTS ---
with tab4:
    st.subheader("Uploaded Data Insights")
    if uploaded_file is not None:
        st.success(f"✅ Active dataset: '{uploaded_file.name}' ({len(df)} rows)")
        with st.container(border=True):
            st.markdown("### Top 3 Performing Suppliers (By Delivery & Quality)")
            # Sort by highest delivery score, then highest quality score
            top_suppliers = df.sort_values(by=["DeliveryScore", "QualityScore"], ascending=[False, False]).head(3)
            st.dataframe(top_suppliers[["Supplier", "OnTimeDelivery", "DefectRate", "ComplianceScore"]], use_container_width=True, hide_index=True)
            
            st.markdown("### Highest Risk Suppliers (By Defect Rate)")
            # Sort by highest defect rate
            risk_suppliers = df.sort_values(by="DefectRate", ascending=False).head(3)
            st.dataframe(risk_suppliers[["Supplier", "DefectRate", "OnTimeDelivery", "CostVariance"]], use_container_width=True, hide_index=True)
            
            st.markdown("### Dataset Statistical Profile")
            st.dataframe(df.describe().T, use_container_width=True)
    else:
        st.info("ℹ️ You are currently viewing the default system data. Upload a custom CSV file via the sidebar to generate custom insights here.")

# --- TAB 5: INSTRUCTIONS ---
with tab5:
    st.subheader("Getting Started")
    with st.container(border=True):
        st.markdown("""
        ### Choose your analysis method:

        **Weighted Risk Scoring Method**
        • Customize weights for each KPI factor
        • Get weighted risk scores and categorization
        • Real-time interactive dashboards
        • Filter suppliers by risk level

        > Navigate to **Weighted Method** in the sidebar

        **Data Envelopment Analysis (DEA)**
        • Identify efficiency frontiers
        • Benchmark suppliers against each other
        • Input-output optimization analysis
        • Detailed efficiency rankings

        > Navigate to **DEA Analysis** in the sidebar
        """)

st.divider()

# ============ DOWNLOAD OPTION ============
st.subheader("Export Current Data")
st.write("Download the active dataset (includes calculated KPI scores).")

st.download_button(
    label="📥 Download Data (CSV)",
    data=df.to_csv(index=False),
    file_name="supplier_data_export.csv",
    mime="text/csv",
    use_container_width=True
)