import pandas as pd
import streamlit as st
from utils import load_supplier_data, calculate_kpi_scores, compute_dea, dea_classify

st.set_page_config(page_title="DEA Analysis", layout="wide")

st.title("Data Envelopment Analysis (DEA)")
st.markdown("### Efficiency frontier analysis for supplier evaluation")

# Load data
df = load_supplier_data()
df = calculate_kpi_scores(df)

# ============ DEA INFORMATION ============
with st.expander("About DEA Model"):
    st.markdown("""
    **Data Envelopment Analysis (DEA)** is a linear programming technique that evaluates 
    relative efficiency of decision-making units (suppliers).
    
    **Model Type:** Input-Oriented CCR Model
    
    **Inputs (to minimize):**
    - Cost Variance: Target cost adherence
    - Defect Rate: Quality consistency
    
    **Outputs (to maximize):**
    - On-Time Delivery: Timeliness performance
    - Compliance Score: Regulatory adherence
    
    **Efficiency Score:** 0 to 1 (1 = frontier efficiency)
    """)

# ============ DEA COMPUTATION ============
st.sidebar.header("DEA Configuration")

if st.sidebar.button("Run DEA Analysis", use_container_width=True):
    with st.spinner("Computing DEA efficiency scores..."):
        df["DEA_Efficiency"] = compute_dea(df)
        df["DEA_Category"] = df["DEA_Efficiency"].apply(dea_classify)
        st.session_state.dea_computed = True
        st.session_state.dea_df = df
    st.sidebar.success("DEA computation complete!")
else:
    if "dea_computed" in st.session_state and st.session_state.dea_computed:
        df = st.session_state.dea_df

# ============ DISPLAY RESULTS ============
if "DEA_Efficiency" in df.columns:
    # Sort by efficiency
    df = df.sort_values("DEA_Efficiency", ascending=False)
    
    # ============ KPI METRICS ============
    st.subheader("Efficiency Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_efficiency = df["DEA_Efficiency"].mean()
        st.metric("Average Efficiency", f"{avg_efficiency:.3f}")
    
    with col2:
        st.metric("Efficient Suppliers", (df["DEA_Category"] == "Efficient").sum())
    
    with col3:
        st.metric("Moderate Suppliers", (df["DEA_Category"] == "Moderate").sum())
    
    with col4:
        st.metric("Inefficient Suppliers", (df["DEA_Category"] == "Inefficient").sum())
    
    # ============ CATEGORY DISTRIBUTION ============
    st.subheader("Efficiency Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        category_counts = df["DEA_Category"].value_counts()
        st.bar_chart(category_counts)
    
    with col2:
        st.markdown("**Category Breakdown:**")
        for category in ["Efficient", "Moderate", "Inefficient"]:
            count = (df["DEA_Category"] == category).sum()
            pct = (count / len(df)) * 100
            st.write(f"• {category}: {count} suppliers ({pct:.1f}%)")
    
    # ============ EFFICIENCY RANKING ============
    st.subheader("Supplier Efficiency Ranking")
    
    # Filter option
    filter_category = st.selectbox(
        "Filter by Efficiency Category",
        ["All", "Efficient", "Moderate", "Inefficient"]
    )
    
    if filter_category != "All":
        display_df = df[df["DEA_Category"] == filter_category].copy()
    else:
        display_df = df.copy()
    
    # Display table
    table_cols = ["Supplier", "DEA_Efficiency", "DEA_Category"]
    display_table = display_df[table_cols].copy()
    display_table["DEA_Efficiency"] = display_table["DEA_Efficiency"].round(3)
    display_table = display_table.reset_index(drop=True)
    
    st.dataframe(display_table, use_container_width=True)
    
    # ============ EFFICIENCY CHART ============
    st.subheader("Efficiency Scores (All Suppliers)")
    efficiency_chart = df[["Supplier", "DEA_Efficiency"]].copy()
    efficiency_chart = efficiency_chart.set_index("Supplier")
    st.bar_chart(efficiency_chart)
    
    # ============ INPUT-OUTPUT RELATIONSHIP ============
    st.subheader("Input-Output Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Cost Variance vs On-Time Delivery**")
        io_data = df[["Supplier", "CostVariance", "OnTimeDelivery"]].copy()
        io_data = io_data.rename(columns={"CostVariance": "Cost Variance", "OnTimeDelivery": "Delivery"})
        st.scatter_chart(io_data.set_index("Supplier"))
    
    with col2:
        st.write("**Defect Rate vs Compliance Score**")
        io_data2 = df[["Supplier", "DefectRate", "ComplianceScore"]].copy()
        io_data2 = io_data2.rename(columns={"DefectRate": "Defect Rate", "ComplianceScore": "Compliance"})
        st.scatter_chart(io_data2.set_index("Supplier"))
    
    # ============ EFFICIENCY FRONTIER ============
    st.subheader("Efficiency Frontier Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        efficient_suppliers = df[df["DEA_Category"] == "Efficient"]
        st.write(f"**Frontier Suppliers ({len(efficient_suppliers)}):**")
        if len(efficient_suppliers) > 0:
            for idx, row in efficient_suppliers.iterrows():
                st.write(f"• {row['Supplier']} - Score: {row['DEA_Efficiency']:.3f}")
        else:
            st.info("No fully efficient suppliers in dataset")
    
    with col2:
        st.write("**Improvement Opportunities:**")
        improvement_suppliers = df[df["DEA_Category"] == "Inefficient"].head(3)
        if len(improvement_suppliers) > 0:
            st.write("Top 3 suppliers needing improvement:")
            for idx, row in improvement_suppliers.iterrows():
                gap = 1.0 - row["DEA_Efficiency"]
                st.write(f"• {row['Supplier']}: {gap:.1%} efficiency gap")
        else:
            st.info("All suppliers above inefficient threshold")
    
    # ============ INSIGHTS ============
    st.subheader("Key Insights")
    
    best_idx = df["DEA_Efficiency"].idxmax()
    worst_idx = df["DEA_Efficiency"].idxmin()
    
    best = df.loc[best_idx]
    worst = df.loc[worst_idx]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"""
        **Most Efficient: {best['Supplier']}**
        - DEA Efficiency: {best['DEA_Efficiency']:.3f}
        - Category: {best['DEA_Category']}
        """)
    
    with col2:
        st.warning(f"""
        **Least Efficient: {worst['Supplier']}**
        - DEA Efficiency: {worst['DEA_Efficiency']:.3f}
        - Category: {worst['DEA_Category']}
        """)
    
    # ============ EXPORT ============
    st.subheader("Export Data")
    st.download_button(
        label="Download DEA Report (CSV)",
        data=df.to_csv(index=False),
        file_name="dea_analysis_report.csv",
        mime="text/csv"
    )

else:
    st.info("Click 'Run DEA Analysis' in the sidebar to compute efficiency scores")
