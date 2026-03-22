# Supplier Evaluation & Risk Scoring System

Multi-page Streamlit dashboard for supplier performance analysis using two evaluation methods.

## Quick Start

```bash
# Install dependencies
pip install streamlit pandas pulp

# Run dashboard
streamlit run app.py
```

Dashboard runs at `http://localhost:8501`

## Features

### Home Page
- Dataset overview and statistics
- Raw supplier data view
- Navigation to analysis methods

### Weighted Risk Scoring Method
- Customize KPI weights (Delivery, Quality, Cost, Compliance)
- Real-time risk score calculation
- Filter by risk category (Low/Medium/High)
- Trend analysis and insights

### DEA Analysis
- Data Envelopment Analysis using input-oriented CCR model
- Efficiency frontier identification
- Supplier benchmarking
- Improvement opportunity analysis

## Project Structure

```
Major_project/
├── app.py                    # Home page
├── utils.py                  # Shared functions
├── suppliers.csv             # Sample data
├── suppliers_large_approx100k.csv  # Large dataset
└── pages/
    ├── 1_weighted_method.py  # Weighted scoring
    └── 2_dea_analysis.py     # DEA analysis
```

## Data

**Input columns:**
- Supplier: Supplier name
- OnTimeDelivery: Percentage (0-100)
- DefectRate: Percentage (0-100)
- CostVariance: Percentage (0-100)
- ComplianceScore: Score (0-100)

**Calculated scores:**
- DeliveryScore = OnTimeDelivery / 100
- QualityScore = 1 - (DefectRate / 100)
- CostScore = 1 - (CostVariance / 100)
- ComplianceScoreNorm = ComplianceScore / 100

## Methods

### Weighted Scoring
Combines normalized KPI scores with user-defined weights.

```
RiskScore = (w1 × DeliveryScore) + (w2 × QualityScore) + (w3 × CostScore) + (w4 × ComplianceScore)
```

**Categories:**
- Low Risk: ≥ 0.8
- Medium Risk: 0.6 - 0.79
- High Risk: < 0.6

### DEA Analysis
Linear programming optimization for efficiency evaluation.

**Inputs (minimize):**
- CostVariance
- DefectRate

**Outputs (maximize):**
- OnTimeDelivery
- ComplianceScore

**Efficiency Categories:**
- Efficient: ≥ 0.9
- Moderate: 0.7 - 0.89
- Inefficient: < 0.7

## Dependencies

- `streamlit` - Web framework
- `pandas` - Data handling
- `pulp` - Linear programming

## Usage

1. Navigate to **Weighted Method** to customize risk scoring
2. Adjust weight sliders to reflect business priorities
3. View risk distribution and supplier rankings
4. Switch to **DEA Analysis** for efficiency evaluation
5. Click "Run DEA Analysis" to compute efficiency scores
6. Download reports as CSV from either page

## Notes

- Supports datasets up to ~100k suppliers
- DEA computation time varies with dataset size
- Data normalized automatically for calculation
- All weights must sum to 1.0 in weighted method
