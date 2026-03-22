"""
Shared utilities for Supplier Evaluation System
"""
import pandas as pd
from pulp import *


def compute_dea(df):
    """
    Compute Data Envelopment Analysis (DEA) efficiency scores using CCR model.
    
    Input-oriented model:
    - Inputs: CostVariance, DefectRate (to minimize)
    - Outputs: OnTimeDelivery, ComplianceScore (to maximize)
    
    Returns: List of efficiency scores (0-1) for each supplier
    """
    efficiency_scores = []
    
    # Normalize data to avoid numerical issues
    df_norm = df.copy()
    df_norm["CostVariance"] = df["CostVariance"] / 100
    df_norm["DefectRate"] = df["DefectRate"] / 100
    df_norm["OnTimeDelivery"] = df["OnTimeDelivery"] / 100
    df_norm["ComplianceScore"] = df["ComplianceScore"] / 100
    
    num_suppliers = len(df)
    
    # Solve DEA for each supplier
    for i in range(num_suppliers):
        # Create linear programming problem
        prob = LpProblem(f"DEA_Supplier_{i}", LpMaximize)
        
        # Decision variables: input and output weights
        u1 = LpVariable("u1", lowBound=0)  # Weight for OnTimeDelivery
        u2 = LpVariable("u2", lowBound=0)  # Weight for ComplianceScore
        v1 = LpVariable("v1", lowBound=0)  # Weight for CostVariance
        v2 = LpVariable("v2", lowBound=0)  # Weight for DefectRate
        
        # Objective: Maximize efficiency of supplier i
        prob += u1 * df_norm.iloc[i]["OnTimeDelivery"] + u2 * df_norm.iloc[i]["ComplianceScore"]
        
        # Constraint 1: Normalized input (denominator) equals 1
        prob += v1 * df_norm.iloc[i]["CostVariance"] + v2 * df_norm.iloc[i]["DefectRate"] == 1
        
        # Constraint 2: Efficiency of all suppliers <= 1
        for j in range(num_suppliers):
            prob += (u1 * df_norm.iloc[j]["OnTimeDelivery"] + 
                     u2 * df_norm.iloc[j]["ComplianceScore"]) <= \
                    (v1 * df_norm.iloc[j]["CostVariance"] + 
                     v2 * df_norm.iloc[j]["DefectRate"])
        
        # Solve (suppress output)
        prob.solve(PULP_CBC_CMD(msg=0))
        
        # Extract efficiency score
        if prob.status == 1:  # Optimal solution found
            efficiency = value(prob.objective)
            efficiency_scores.append(min(efficiency, 1.0))  # Cap at 1.0
        else:
            efficiency_scores.append(0.0)  # Handle infeasible cases
    
    return efficiency_scores


def dea_classify(score):
    """Classify suppliers based on DEA efficiency score"""
    if score >= 0.9:
        return "Efficient"
    elif score >= 0.7:
        return "Moderate"
    else:
        return "Inefficient"


def classify_risk(score):
    """Classify suppliers based on risk score"""
    if score >= 0.8:
        return "Low Risk"
    elif score >= 0.6:
        return "Medium Risk"
    else:
        return "High Risk"


def load_supplier_data():
    """Load supplier data from CSV"""
    return pd.read_csv("suppliers.csv")


def calculate_kpi_scores(df):
    """Calculate KPI scores for suppliers"""
    df_copy = df.copy()
    df_copy["DeliveryScore"] = df_copy["OnTimeDelivery"] / 100
    df_copy["QualityScore"] = 1 - (df_copy["DefectRate"] / 100)
    df_copy["CostScore"] = 1 - (df_copy["CostVariance"] / 100)
    df_copy["ComplianceScoreNorm"] = df_copy["ComplianceScore"] / 100
    return df_copy
