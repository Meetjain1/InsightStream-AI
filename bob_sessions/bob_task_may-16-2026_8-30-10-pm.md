# 📊 EDA Utils - Comprehensive Guide

## Overview
The `eda_utils.py` module provides a complete suite of exploratory data analysis tools for customer churn prediction, featuring interactive Plotly visualizations, statistical analysis, and business insights.

---

## 🎯 Module Structure

### 1. **Core Visualization Functions**
Basic building blocks for churn analysis

### 2. **KPI Summary Functions**
Business metrics and dashboard creation

### 3. **Advanced Distribution Analysis**
Statistical comparisons and pattern detection

### 4. **Customer Segmentation**
Hierarchical and multi-dimensional views

### 5. **Multi-Dimensional Analysis**
Complex relationship exploration

### 6. **Time-Based Analysis**
Cohort and lifecycle patterns

### 7. **Feature Importance**
Predictive power assessment

### 8. **Interactive Explorers**
Dynamic drill-down capabilities

---

## 📚 Function Reference

### Core Visualizations

#### `create_churn_donut(df)`
**Purpose:** Create donut chart showing overall churn rate

**Parameters:**
- `df`: DataFrame with churn data

**Returns:**
- `fig`: Plotly figure object
- `interpretation`: Business insight string

**Example:**
```python
fig, insight = create_churn_donut(customer_df)
st.plotly_chart(fig)
st.info(insight)
```

**Output:** Donut chart with churn percentage in center

---

#### `create_categorical_churn_plots(df, cat_col)`
**Purpose:** Analyze churn rates across categorical variables

**Parameters:**
- `df`: DataFrame
- `cat_col`: Categorical column name (e.g., 'region', 'payment_type')

**Returns:**
- `fig`: Bar chart with churn rates
- `interpretation`: Key findings

**Use Cases:**
- Compare churn by region
- Analyze payment method impact
- Identify high-risk segments

---

#### `create_numeric_histogram(df, num_col)`
**Purpose:** Compare distributions of numeric features between churned and retained customers

**Parameters:**
- `df`: DataFrame
- `num_col`: Numeric column name

**Returns:**
- `fig`: Overlaid histogram
- `interpretation`: Statistical comparison

**Best For:**
- Age distribution analysis
- Order value patterns
- Loyalty score comparison

---

#### `create_correlation_heatmap(df)`
**Purpose:** Visualize correlations between all numeric features

**Returns:**
- `fig`: Interactive heatmap
- `interpretation`: Top correlations with churn

**Insights:**
- Feature relationships
- Multicollinearity detection
- Churn predictors

---

### KPI Functions

#### `calculate_kpi_summary(df)`
**Purpose:** Calculate comprehensive business metrics

**Returns:** Dictionary with:
```python
{
    'total_customers': int,
    'churn_rate': float,
    'retention_rate': float,
    'avg_customer_value': float,
    'churned_value_loss': float,
    'avg_loyalty_score': float,
    'complaint_rate': float,
    'inactive_rate': float,
    'avg_tenure': float,
    # ... and more
}
```

**Usage:**
```python
kpis = calculate_kpi_summary(df)
st.metric("Churn Rate", f"{kpis['churn_rate']:.1f}%")
st.metric("Avg Customer Value", f"${kpis['avg_customer_value']:.2f}")
```

---

#### `create_kpi_dashboard(df)`
**Purpose:** Create visual KPI dashboard with 8 key metrics

**Returns:**
- `fig`: Multi-indicator dashboard
- `interpretation`: Overall health assessment

**Displays:**
1. Total Customers
2. Churn Rate (with delta)
3. Avg Customer Value
4. Retention Rate (with delta)
5. Avg Loyalty Score
6. Complaint Rate
7. Inactive Rate
8. Avg Tenure

**Perfect For:** Executive summaries and overview pages

---

### Advanced Distribution Analysis

#### `create_box_plot_comparison(df, numeric_col)`
**Purpose:** Statistical comparison with outlier detection

**Features:**
- Box plots for churned vs retained
- Mean and standard deviation markers
- Statistical significance testing (t-test)

**Returns:**
- `fig`: Box plot comparison
- `interpretation`: Statistical test results (p-value)

**Interpretation Guide:**
- p < 0.05: Significant difference (strong predictor)
- p ≥ 0.05: No significant difference

---

#### `create_violin_plot(df, numeric_col)`
**Purpose:** Detailed probability density visualization

**Shows:**
- Full distribution shape
- Density at each value
- Outliers
- Quartiles

**Best For:** Understanding distribution nuances

---

### Customer Segmentation

#### `create_customer_segment_sunburst(df)`
**Purpose:** Hierarchical customer segmentation visualization

**Hierarchy:** Region → Payment Type → Churn Status

**Features:**
- Interactive drill-down
- Click to zoom
- Proportional sizing

**Use Cases:**
- Identify high-risk segments
- Understand customer composition
- Regional analysis

---

#### `create_treemap_analysis(df)`
**Purpose:** Value-based customer segmentation

**Visualization:**
- Size = Customer count
- Color = Average order value
- Hierarchy = Region → Payment Type → Churn Status

**Color Scale:**
- Green = High value customers
- Yellow = Medium value
- Red = Low value (focus areas!)

---

### Multi-Dimensional Analysis

#### `create_parallel_coordinates(df)`
**Purpose:** Visualize multiple features simultaneously

**Features:**
- Each line = one customer
- Color = Churn status (red = churned)
- Interactive filtering

**How to Read:**
- Look for red line clusters
- Identify common patterns in churned customers
- Spot feature combinations leading to churn

**Best For:** Pattern discovery across multiple dimensions

---

#### `create_scatter_matrix(df)`
**Purpose:** Pairwise feature relationship analysis

**Shows:**
- All feature combinations
- Correlation patterns
- Separation between churned/retained

**Features:**
- 5 key numeric features
- Color-coded by churn status
- Interactive zoom and pan

---

### Time-Based Analysis

#### `create_cohort_analysis(df)`
**Purpose:** Analyze churn patterns across customer lifecycle

**Cohorts:**
- 0-3 months (New customers)
- 3-6 months (Early stage)
- 6-12 months (Established)
- 1-2 years (Loyal)
- 2-3 years (Very loyal)
- 3+ years (Champions)

**Displays:**
- Churn rate by cohort
- Customer count by cohort
- Critical retention periods

**Key Insight:** Identifies when customers are most likely to churn

---

#### `create_days_buckets_chart(df)`
**Purpose:** Analyze churn by recency

**Buckets:**
- 0-30 days (Recent)
- 31-60 days (Active)
- 61-90 days (At risk)
- 90+ days (Inactive)

**Action Items:** Target customers in high-churn buckets

---

#### `create_tenure_churn_plot(df)`
**Purpose:** Churn rate by customer tenure

**Insights:**
- Early churn patterns
- Loyalty development
- Critical retention windows

---

### Feature Importance

#### `create_feature_importance_chart(df)`
**Purpose:** Identify strongest churn predictors

**Method:** Correlation analysis with churn

**Visualization:**
- Horizontal bar chart
- Red bars = Positive correlation (increases churn)
- Blue bars = Negative correlation (decreases churn)

**Use Cases:**
- Feature selection for modeling
- Business strategy prioritization
- Understanding churn drivers

---

### Interactive Explorers

#### `create_interactive_churn_explorer(df)`
**Purpose:** Dynamic multi-dimensional exploration

**Features:**
- Bubble chart (size = customer count)
- Faceted by region and payment type
- X-axis = Average order value
- Y-axis = Average loyalty score
- Color = Churn status

**How to Use:**
1. Identify red bubbles (churned customers)
2. Look for patterns in specific segments
3. Focus on large red bubbles (high-risk, high-volume)

---

### Comprehensive Reports

#### `create_eda_plots(df)`
**Purpose:** Generate standard EDA report (original function)

**Returns:** List of plot dictionaries with:
- title
- plot (Plotly figure)
- interpretation

**Includes:**
- Churn donut
- Categorical analyses
- Numeric distributions
- Correlation heatmap
- Pattern analyses

---

#### `generate_comprehensive_eda_report(df)`
**Purpose:** Generate complete EDA report with ALL visualizations

**Returns:** List of categorized plots:

**Categories:**
- `overview`: KPI dashboard, churn rate
- `importance`: Feature importance
- `correlation`: Heatmaps
- `categorical`: Churn by categories
- `distribution`: Histograms, box plots
- `cohort`: Lifecycle analysis
- `segmentation`: Sunburst, treemap
- `multidimensional`: Parallel coordinates, scatter matrix
- `patterns`: Days since purchase, tenure, loyalty
- `interactive`: Explorers

**Usage:**
```python
all_plots = generate_comprehensive_eda_report(df)

# Filter by category
overview_plots = [p for p in all_plots if p['category'] == 'overview']

# Display all
for plot_info in all_plots:
    st.subheader(plot_info['title'])
    st.plotly_chart(plot_info['plot'])
    st.info(plot_info['interpretation'])
```

---

## 🎨 Visualization Best Practices

### Color Scheme
- **Churned:** `#FF6B6B` (Red) - Danger, attention needed
- **Retained:** `#4ECDC4` (Teal) - Success, healthy
- **Neutral:** `#FFD166` (Yellow) - Warning, moderate

### Interactive Features
All Plotly charts support:
- Zoom and pan
- Hover for details
- Click to filter
- Download as PNG
- Responsive sizing

### Performance Tips
1. **Large Datasets:** Functions automatically sample data when needed
   - Parallel coordinates: Max 1000 rows
   - Scatter matrix: Max 500 rows

2. **Missing Data:** All functions handle missing values gracefully

3. **Column Validation:** Functions check for required columns before processing

---

## 📊 Usage Examples

### Example 1: Quick Overview Dashboard
```python
import streamlit as st
from src.eda_utils import create_kpi_dashboard, create_churn_donut

# Load data
df = load_customer_data()

# Create dashboard
st.title("Customer Churn Overview")

# KPI Dashboard
kpi_fig, kpi_insight = create_kpi_dashboard(df)
st.plotly_chart(kpi_fig, use_container_width=True)
st.info(kpi_insight)

# Churn rate
donut_fig, donut_insight = create_churn_donut(df)
col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(donut_fig)
with col2:
    st.metric("Churn Rate", f"{df['churn'].mean()*100:.1f}%")
    st.info(donut_insight)
```

### Example 2: Feature Analysis
```python
from src.eda_utils import (
    create_feature_importance_chart,
    create_box_plot_comparison,
    create_correlation_heatmap
)

st.title("Feature Analysis")

# Feature importance
feat_fig, feat_insight = create_feature_importance_chart(df)
st.plotly_chart(feat_fig, use_container_width=True)
st.success(feat_insight)

# Detailed analysis for top features
top_features = ['loyalty_score', 'days_since_last_purchase', 'complaints']

for feature in top_features:
    st.subheader(f"Analysis: {feature}")
    
    # Box plot with statistical test
    box_fig, box_insight = create_box_plot_comparison(df, feature)
    st.plotly_chart(box_fig)
    st.info(box_insight)

# Correlation heatmap
corr_fig, corr_insight = create_correlation_heatmap(df)
st.plotly_chart(corr_fig, use_container_width=True)
st.info(corr_insight)
```

### Example 3: Customer Segmentation
```python
from src.eda_utils import (
    create_customer_segment_sunburst,
    create_treemap_analysis,
    create_cohort_analysis
)

st.title("Customer Segmentation Analysis")

# Sunburst
st.subheader("🌞 Customer Hierarchy")
sunburst_fig, sunburst_insight = create_customer_segment_sunburst(df)
st.plotly_chart(sunburst_fig, use_container_width=True)
st.info(sunburst_insight)

# Treemap
st.subheader("🗺️ Value Distribution")
treemap_fig, treemap_insight = create_treemap_analysis(df)
st.plotly_chart(treemap_fig, use_container_width=True)
st.info(treemap_insight)

# Cohort analysis
st.subheader("👥 Lifecycle Analysis")
cohort_fig, cohort_insight = create_cohort_analysis(df)
st.plotly_chart(cohort_fig, use_container_width=True)
st.warning(cohort_insight)
```

### Example 4: Complete EDA Report
```python
from src.eda_utils import generate_comprehensive_eda_report

st.title("Complete EDA Report")

# Generate all plots
all_plots = generate_comprehensive_eda_report(df)

# Create tabs by category
categories = list(set(p['category'] for p in all_plots))
tabs = st.tabs(categories)

for tab, category in zip(tabs, categories):
    with tab:
        category_plots = [p for p in all_plots if p['category'] == category]
        
        for plot_info in category_plots:
            st.subheader(plot_info['title'])
            st.plotly_chart(plot_info['plot'], use_container_width=True)
            st.info(plot_info['interpretation'])
            st.divider()
```

---

## 🔧 Customization Guide

### Adding New Visualizations

```python
def create_custom_analysis(df):
    """
    Template for custom visualization
    """
    # 1. Validate input
    if df is None or df.empty:
        return None, None
    
    # 2. Check required columns
    required_cols = ['your_column', TARGET_COL]
    if not all(col in df.columns for col in required_cols):
        return None, None
    
    # 3. Process data
    # Your data processing here
    
    # 4. Create Plotly figure
    fig = px.bar(...)  # or any Plotly chart
    
    # 5. Customize layout
    fig.update_layout(
        title="Your Title",
        height=500,
        # ... other settings
    )
    
    # 6. Generate interpretation
    interpretation = "Your business insight here"
    
    return fig, interpretation
```

### Modifying Color Schemes

```python
# Define custom colors
CUSTOM_COLORS = {
    'churned': '#YOUR_COLOR',
    'retained': '#YOUR_COLOR',
    'neutral': '#YOUR_COLOR'
}

# Use in visualizations
fig = px.bar(
    ...,
    color_discrete_map={
        'Churned': CUSTOM_COLORS['churned'],
        'Retained': CUSTOM_COLORS['retained']
    }
)
```

---

## 📈 Performance Metrics

### Function Execution Times (Approximate)
- `create_churn_donut`: < 0.1s
- `create_kpi_dashboard`: < 0.5s
- `create_correlation_heatmap`: 0.5-2s (depends on features)
- `create_scatter_matrix`: 1-3s (sampled data)
- `generate_comprehensive_eda_report`: 5-15s (all plots)

### Memory Usage
- Small datasets (< 10K rows): Minimal impact
- Medium datasets (10K-100K rows): Moderate (sampling used)
- Large datasets (> 100K rows): Automatic sampling for complex plots

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** "Column not found" error
**Solution:** Check that your DataFrame has the required columns from `helpers.py`

**Issue:** Empty plots
**Solution:** Verify data is not None and has rows

**Issue:** Slow performance
**Solution:** Functions automatically sample large datasets, but you can pre-filter

**Issue:** Import errors
**Solution:** Ensure all dependencies are installed:
```bash
pip install pandas numpy plotly scipy matplotlib seaborn
```

---

## 🎯 Best Practices

1. **Always check return values** - Functions return `None, None` if data is invalid
2. **Use interpretations** - Display the interpretation text for business context
3. **Combine visualizations** - Use multiple plots for comprehensive analysis
4. **Filter data appropriately** - Pre-filter data for specific segments
5. **Cache results** - Use Streamlit's `@st.cache_data` for expensive operations

---

## 📝 Notes

- All functions are designed to be **fail-safe** - they return `None, None` instead of raising errors
- **Interpretations** are written in casual, business-friendly language
- **Color consistency** across all visualizations for better UX
- **Interactive features** enabled by default in all Plotly charts
- **Statistical tests** included where appropriate (t-tests, correlations)

---

## 🚀 Future Enhancements

Potential additions:
- Time series analysis for temporal patterns
- Predictive modeling integration
- A/B test analysis tools
- Customer journey mapping
- Automated insight generation with ML
- Export to PDF/PowerPoint
- Real-time dashboard updates

---

## 📚 Related Documentation

- `helpers.py` - Column definitions and business rules
- `data_prep.py` - Data preprocessing functions
- `biz_metrics.py` - Business metric calculations
- `sql_utils.py` - Database operations

---

**© 2026 | Project created by Meet Jain(@Meetjain1) and Aditi Gopinath(@aaditiiiii1)**

**Last Updated:** May 16, 2026
**Version:** 2.0 - Comprehensive Enhancement