"""
EDA Utilities for Customer Churn Prediction App

This module provides comprehensive exploratory data analysis tools including:
- Interactive Plotly visualizations
- Statistical summaries and KPI dashboards
- Correlation analysis and feature importance
- Customer distribution and segmentation charts
- Churn pattern analysis across multiple dimensions

All functions return Plotly figures for interactive exploration and
interpretations for business insights.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

from .helpers import NUMERIC_COLS, CATEGORICAL_COLS, TARGET_COL, FEATURE_COLS

def create_churn_donut(df):
    """
    Create a donut chart for churn distribution
    """
    if df is None or df.empty or TARGET_COL not in df.columns:
        return None, None
    
    # Calculate churn rate
    churn_count = df[TARGET_COL].sum()
    total_count = len(df)
    churn_rate = churn_count / total_count * 100
    retain_rate = 100 - churn_rate
    
    # Create donut chart with Plotly
    labels = ['Churned', 'Retained']
    values = [churn_rate, retain_rate]
    colors = ['#FF6B6B', '#4ECDC4']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.5,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title_text=f"Churn Rate: {churn_rate:.1f}%",
        annotations=[dict(text=f"{churn_rate:.1f}%", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    interpretation = f"We're losing {churn_rate:.1f}% of customers. need to fix that!"
    
    return fig, interpretation

def create_categorical_churn_plots(df, cat_col):
    """
    Create bar chart for churn by categorical column
    """
    if df is None or df.empty or cat_col not in df.columns or TARGET_COL not in df.columns:
        return None, None
    
    # Calculate churn rate by category
    churn_by_cat = df.groupby(cat_col)[TARGET_COL].mean() * 100
    counts_by_cat = df.groupby(cat_col).size()
    
    # Create DataFrame for plotting
    plot_df = pd.DataFrame({
        'ChurnRate': churn_by_cat,
        'Count': counts_by_cat
    }).reset_index()
    
    # Sort by churn rate
    plot_df = plot_df.sort_values('ChurnRate', ascending=False)
    
    # Create bar chart with Plotly
    fig = px.bar(
        plot_df,
        x=cat_col,
        y='ChurnRate',
        text=plot_df['ChurnRate'].apply(lambda x: f"{x:.1f}%"),
        color='ChurnRate',
        color_continuous_scale=['#4ECDC4', '#FFD166', '#FF6B6B'],
        hover_data=['Count'],
        title=f"Churn Rate by {cat_col}"
    )
    
    fig.update_layout(
        xaxis_title=cat_col,
        yaxis_title="Churn Rate (%)",
        yaxis=dict(range=[0, max(plot_df['ChurnRate']) * 1.1])
    )
    
    # Simple interpretation
    highest_cat = plot_df.iloc[0][cat_col]
    lowest_cat = plot_df.iloc[-1][cat_col]
    highest_rate = plot_df.iloc[0]['ChurnRate']
    lowest_rate = plot_df.iloc[-1]['ChurnRate']
    
    interpretation = f"{highest_cat} has highest churn ({highest_rate:.1f}%), while {lowest_cat} has lowest ({lowest_rate:.1f}%). big difference!"
    
    return fig, interpretation

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

def create_numeric_histogram(df, num_col):
    """
    Create histogram for numeric column by churn status
    """
    if df is None or df.empty or num_col not in df.columns or TARGET_COL not in df.columns:
        return None, None
    
    # Create histogram with Plotly
    fig = px.histogram(
        df,
        x=num_col,
        color=df[TARGET_COL].map({0: 'Retained', 1: 'Churned'}),
        barmode='overlay',
        opacity=0.7,
        color_discrete_map={'Retained': '#4ECDC4', 'Churned': '#FF6B6B'},
        title=f"Distribution of {num_col} by Churn Status"
    )
    
    fig.update_layout(
        xaxis_title=num_col,
        yaxis_title="Count",
        legend_title="Customer Status"
    )
    
    # Simple interpretation
    churned_mean = df[df[TARGET_COL] == 1][num_col].mean()
    retained_mean = df[df[TARGET_COL] == 0][num_col].mean()
    
    if churned_mean > retained_mean:
        interpretation = f"Churned customers have higher {num_col} ({churned_mean:.1f} vs {retained_mean:.1f}). interesting!"
    else:
        interpretation = f"Retained customers have higher {num_col} ({retained_mean:.1f} vs {churned_mean:.1f}). makes sense!"
    
    return fig, interpretation

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

def create_correlation_heatmap(df):
    """
    Create correlation heatmap for numeric columns
    """
    if df is None or df.empty:
        return None, None
    
    # Select numeric columns only
    num_cols = [col for col in NUMERIC_COLS if col in df.columns]
    if TARGET_COL in df.columns:
        num_cols.append(TARGET_COL)
    
    if len(num_cols) < 2:
        return None, None
    
    # Calculate correlation matrix
    corr_matrix = df[num_cols].corr()
    
    # Create heatmap with Plotly
    fig = px.imshow(
        corr_matrix,
        text_auto='.2f',
        color_continuous_scale='RdBu_r',
        aspect="auto",
        title="Correlation Heatmap"
    )
    
    fig.update_layout(
        height=600,
        width=700
    )
    
    # Find the most correlated feature with churn
    if TARGET_COL in corr_matrix.columns:
        churn_corr = corr_matrix[TARGET_COL].drop(TARGET_COL)
        top_pos = churn_corr.nlargest(1).index[0]
        top_neg = churn_corr.nsmallest(1).index[0]
        
        interpretation = f"{top_pos} is most positive correlated with churn ({churn_corr[top_pos]:.2f}), and {top_neg} is most negative ({churn_corr[top_neg]:.2f}). this helps!"
    else:
        interpretation = "No direct correlation with churn available. need more data maybe?"
    
    return fig, interpretation

def create_days_buckets_chart(df):
    """
    Create chart for churn by days since last purchase buckets
    """
    if df is None or df.empty or 'days_since_last_purchase' not in df.columns or TARGET_COL not in df.columns:
        return None, None
    
# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
  
    # Create buckets
    bins = [0, 30, 60, 90, float('inf')]
    labels = ['0-30 days', '31-60 days', '61-90 days', 'Over 90 days']
    
    df['days_bucket'] = pd.cut(df['days_since_last_purchase'], bins=bins, labels=labels, right=False)
    
    # Calculate churn rate by bucket
    churn_by_bucket = df.groupby('days_bucket')[TARGET_COL].mean() * 100
    counts_by_bucket = df.groupby('days_bucket').size()
    
    # Create DataFrame for plotting
    plot_df = pd.DataFrame({
        'ChurnRate': churn_by_bucket,
        'Count': counts_by_bucket
    }).reset_index()
    
    # Create bar chart with Plotly
    fig = px.bar(
        plot_df,
        x='days_bucket',
        y='ChurnRate',
        text=plot_df['ChurnRate'].apply(lambda x: f"{x:.1f}%"),
        color='ChurnRate',
        color_continuous_scale=['#4ECDC4', '#FFD166', '#FF6B6B'],
        hover_data=['Count'],
        title="Churn Rate by Days Since Last Purchase"
    )
    
    fig.update_layout(
        xaxis_title="Days Since Last Purchase",
        yaxis_title="Churn Rate (%)",
        yaxis=dict(range=[0, max(plot_df['ChurnRate']) * 1.1])
    )
    
    # Find highest churn rate bucket
    highest_bucket = plot_df.loc[plot_df['ChurnRate'].idxmax()]['days_bucket']
    highest_rate = plot_df.loc[plot_df['ChurnRate'].idxmax()]['ChurnRate']
    
    interpretation = f"Customers who haven't bought in {highest_bucket} churn the most ({highest_rate:.1f}%). gotta reach them faster!"
    
    return fig, interpretation

def create_tenure_churn_plot(df):
    """
    Create chart for churn by tenure buckets
    """
    if df is None or df.empty or 'tenure_months' not in df.columns or TARGET_COL not in df.columns:
        return None, None
    
    # Create buckets
    bins = [0, 6, 12, 24, 36, float('inf')]
    labels = ['0-6 months', '7-12 months', '1-2 years', '2-3 years', '3+ years']
    
    df['tenure_bucket'] = pd.cut(df['tenure_months'], bins=bins, labels=labels, right=False)
    
    # Calculate churn rate by bucket
    churn_by_bucket = df.groupby('tenure_bucket')[TARGET_COL].mean() * 100
    counts_by_bucket = df.groupby('tenure_bucket').size()
    
    # Create DataFrame for plotting
    plot_df = pd.DataFrame({
        'ChurnRate': churn_by_bucket,
        'Count': counts_by_bucket
    }).reset_index()
    
    # Create bar chart with Plotly
    fig = px.bar(
        plot_df,
        x='tenure_bucket',
        y='ChurnRate',
        text=plot_df['ChurnRate'].apply(lambda x: f"{x:.1f}%"),
        color='ChurnRate',
        color_continuous_scale=['#FF6B6B', '#FFD166', '#4ECDC4'],
        hover_data=['Count'],
        title="Churn Rate by Customer Tenure"
    )
    
    fig.update_layout(
        xaxis_title="Tenure",
        yaxis_title="Churn Rate (%)",
        yaxis=dict(range=[0, max(plot_df['ChurnRate']) * 1.1])
    )

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

    # Find highest churn rate bucket
    highest_bucket = plot_df.loc[plot_df['ChurnRate'].idxmax()]['tenure_bucket']
    highest_rate = plot_df.loc[plot_df['ChurnRate'].idxmax()]['ChurnRate']
    
    interpretation = f"Customers in {highest_bucket} churn the most ({highest_rate:.1f}%). gotta keep them happy early on!"
    
    return fig, interpretation

def create_loyalty_complaints_plot(df):
    """
    Create scatter plot for loyalty vs complaints colored by churn
    """
    if df is None or df.empty or 'loyalty_score' not in df.columns or 'complaints' not in df.columns or TARGET_COL not in df.columns:
        return None, None
    
    # Create scatter plot with Plotly
    fig = px.scatter(
        df,
        x='loyalty_score',
        y='complaints',
        color=df[TARGET_COL].map({0: 'Retained', 1: 'Churned'}),
        color_discrete_map={'Retained': '#4ECDC4', 'Churned': '#FF6B6B'},
        opacity=0.7,
        title="Loyalty Score vs Complaints by Churn Status"
    )
    
    fig.update_layout(
        xaxis_title="Loyalty Score",
        yaxis_title="Complaints",
        legend_title="Customer Status"
    )
    
    # Simple interpretation
    interpretation = "Customers with low loyalty and high complaints churn more. fix those complaints fast!"
    
    return fig, interpretation

def create_eda_plots(df):
    """
    Create all EDA plots
    """
    if df is None or df.empty:
        return []
    
    plots = []
    
    # Churn rate donut
    churn_donut, churn_interp = create_churn_donut(df)
    if churn_donut is not None:
        plots.append({
            "title": "Overall Churn Rate",
            "plot": churn_donut,
            "interpretation": churn_interp
        })
    
    # Categorical plots
    for cat_col in CATEGORICAL_COLS:
        if cat_col in df.columns:
            cat_plot, cat_interp = create_categorical_churn_plots(df, cat_col)
            if cat_plot is not None:
                plots.append({
                    "title": f"Churn by {cat_col}",
                    "plot": cat_plot,
                    "interpretation": cat_interp
                })
    
    # Days since last purchase
    days_plot, days_interp = create_days_buckets_chart(df)
    if days_plot is not None:
        plots.append({
            "title": "Churn by Days Since Last Purchase",
            "plot": days_plot,
            "interpretation": days_interp
        })
    
    # Tenure plot
    tenure_plot, tenure_interp = create_tenure_churn_plot(df)
    if tenure_plot is not None:
        plots.append({
            "title": "Churn by Tenure",
            "plot": tenure_plot,
            "interpretation": tenure_interp
        })
    
    # Loyalty vs complaints
    loyalty_plot, loyalty_interp = create_loyalty_complaints_plot(df)
    if loyalty_plot is not None:
        plots.append({
            "title": "Loyalty vs Complaints",
            "plot": loyalty_plot,
            "interpretation": loyalty_interp
        })
    
    # Numeric histograms for key metrics
    for num_col in ['avg_order_value', 'days_since_last_purchase', 'loyalty_score']:
        if num_col in df.columns:
            num_plot, num_interp = create_numeric_histogram(df, num_col)
            if num_plot is not None:
                plots.append({
                    "title": f"Distribution of {num_col}",
                    "plot": num_plot,
                    "interpretation": num_interp
                })
    
    # Correlation heatmap
    corr_plot, corr_interp = create_correlation_heatmap(df)
    if corr_plot is not None:
        plots.append({
            "title": "Feature Correlations",
            "plot": corr_plot,
            "interpretation": corr_interp
        })
    
    return plots

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

# ============================================================================
# KPI SUMMARY FUNCTIONS
# ============================================================================

def calculate_kpi_summary(df):
    """
    Calculate comprehensive KPI summary for churn analysis
    
    Returns dictionary with key metrics:
    - Total customers
    - Churn rate and count
    - Average customer value
    - Risk distribution
    - Engagement metrics
    """
    if df is None or df.empty:
        return None
    
    kpis = {}
    
    # Basic metrics
    kpis['total_customers'] = len(df)
    
    # Churn metrics
    if TARGET_COL in df.columns:
        kpis['churned_count'] = df[TARGET_COL].sum()
        kpis['retained_count'] = len(df) - kpis['churned_count']
        kpis['churn_rate'] = (kpis['churned_count'] / kpis['total_customers']) * 100
        kpis['retention_rate'] = 100 - kpis['churn_rate']
    
    # Customer value metrics
    if 'avg_order_value' in df.columns:
        kpis['avg_customer_value'] = df['avg_order_value'].mean()
        kpis['total_customer_value'] = df['avg_order_value'].sum()
        
        if TARGET_COL in df.columns:
            kpis['churned_value_loss'] = df[df[TARGET_COL] == 1]['avg_order_value'].sum()
            kpis['avg_churned_value'] = df[df[TARGET_COL] == 1]['avg_order_value'].mean()
            kpis['avg_retained_value'] = df[df[TARGET_COL] == 0]['avg_order_value'].mean()
    
    # Engagement metrics
    if 'total_orders' in df.columns:
        kpis['avg_orders'] = df['total_orders'].mean()
        kpis['total_orders'] = df['total_orders'].sum()
    
    if 'days_since_last_purchase' in df.columns:
        kpis['avg_days_since_purchase'] = df['days_since_last_purchase'].mean()
        kpis['inactive_customers'] = len(df[df['days_since_last_purchase'] > 90])
        kpis['inactive_rate'] = (kpis['inactive_customers'] / kpis['total_customers']) * 100
    
    # Loyalty metrics
    if 'loyalty_score' in df.columns:
        kpis['avg_loyalty_score'] = df['loyalty_score'].mean()
        kpis['high_loyalty_count'] = len(df[df['loyalty_score'] >= 7])
        kpis['low_loyalty_count'] = len(df[df['loyalty_score'] <= 3])
    
    # Complaint metrics
    if 'complaints' in df.columns:
        kpis['avg_complaints'] = df['complaints'].mean()
        kpis['customers_with_complaints'] = len(df[df['complaints'] > 0])
        kpis['complaint_rate'] = (kpis['customers_with_complaints'] / kpis['total_customers']) * 100
    
    # Tenure metrics
    if 'tenure_months' in df.columns:
        kpis['avg_tenure'] = df['tenure_months'].mean()
        kpis['new_customers'] = len(df[df['tenure_months'] <= 6])
        kpis['loyal_customers'] = len(df[df['tenure_months'] >= 24])
    
    return kpis

def create_kpi_dashboard(df):
    """
    Create interactive KPI dashboard with key metrics
    
    Returns Plotly figure with multiple indicator cards
    """
    if df is None or df.empty:
        return None, None
    
    kpis = calculate_kpi_summary(df)
    if kpis is None:
        return None, None
    
    # Create subplots for KPI cards
    fig = make_subplots(
        rows=2, cols=4,
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]],
        subplot_titles=("Total Customers", "Churn Rate", "Avg Customer Value", "Retention Rate",
                       "Avg Loyalty Score", "Complaint Rate", "Inactive Rate", "Avg Tenure")
    )
    
    # Row 1
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis.get('total_customers', 0),
        number={'font': {'size': 40}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=1)
    
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=kpis.get('churn_rate', 0),
        number={'suffix': "%", 'font': {'size': 40}},
        delta={'reference': 20, 'relative': False},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=2)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis.get('avg_customer_value', 0),
        number={'prefix': "$", 'font': {'size': 40}, 'valueformat': '.2f'},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=3)
    
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=kpis.get('retention_rate', 0),
        number={'suffix': "%", 'font': {'size': 40}},
        delta={'reference': 80, 'relative': False},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=4)
    
    # Row 2
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis.get('avg_loyalty_score', 0),
        number={'font': {'size': 40}, 'valueformat': '.1f'},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=2, col=1)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis.get('complaint_rate', 0),
        number={'suffix': "%", 'font': {'size': 40}, 'valueformat': '.1f'},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=2, col=2)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis.get('inactive_rate', 0),
        number={'suffix': "%", 'font': {'size': 40}, 'valueformat': '.1f'},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=2, col=3)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis.get('avg_tenure', 0),
        number={'suffix': " mo", 'font': {'size': 40}, 'valueformat': '.1f'},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=2, col=4)
    
    fig.update_layout(
        height=500,
        title_text="Customer Churn KPI Dashboard",
        title_font_size=24
    )
    
    interpretation = f"Overall health check: {kpis.get('churn_rate', 0):.1f}% churn rate with ${kpis.get('avg_customer_value', 0):.2f} avg value. {kpis.get('complaint_rate', 0):.1f}% have complaints - that's a red flag!"
    
    return fig, interpretation

# ============================================================================
# ADVANCED DISTRIBUTION ANALYSIS
# ============================================================================

def create_box_plot_comparison(df, numeric_col):
    """
    Create box plot comparing churned vs retained customers for a numeric feature
    
    Shows distribution, outliers, and statistical differences
    """
    if df is None or df.empty or numeric_col not in df.columns or TARGET_COL not in df.columns:
        return None, None
    
    # Create box plot
    fig = go.Figure()
    
    # Retained customers
    fig.add_trace(go.Box(
        y=df[df[TARGET_COL] == 0][numeric_col],
        name='Retained',
        marker_color='#4ECDC4',
        boxmean='sd'
    ))
    
    # Churned customers
    fig.add_trace(go.Box(
        y=df[df[TARGET_COL] == 1][numeric_col],
        name='Churned',
        marker_color='#FF6B6B',
        boxmean='sd'
    ))
    
    fig.update_layout(
        title=f"Distribution of {numeric_col} by Churn Status",
        yaxis_title=numeric_col,
        showlegend=True,
        height=500
    )
    
    # Statistical test
    retained_vals = df[df[TARGET_COL] == 0][numeric_col].dropna()
    churned_vals = df[df[TARGET_COL] == 1][numeric_col].dropna()
    
    if len(retained_vals) > 0 and len(churned_vals) > 0:
        t_stat, p_value = stats.ttest_ind(retained_vals, churned_vals)
        
        if p_value < 0.05:
            interpretation = f"Significant difference detected (p={p_value:.4f})! Churned customers have different {numeric_col} patterns. This is a key predictor!"
        else:
            interpretation = f"No significant difference (p={p_value:.4f}). {numeric_col} might not be a strong churn indicator."
    else:
        interpretation = f"Box plot shows distribution of {numeric_col} across customer segments."
    
    return fig, interpretation

def create_violin_plot(df, numeric_col):
    """
    Create violin plot for detailed distribution analysis
    
    Shows probability density and distribution shape
    """
    if df is None or df.empty or numeric_col not in df.columns or TARGET_COL not in df.columns:
        return None, None
    
    fig = px.violin(
        df,
        y=numeric_col,
        x=df[TARGET_COL].map({0: 'Retained', 1: 'Churned'}),
        color=df[TARGET_COL].map({0: 'Retained', 1: 'Churned'}),
        color_discrete_map={'Retained': '#4ECDC4', 'Churned': '#FF6B6B'},
        box=True,
        points='outliers',
        title=f"Violin Plot: {numeric_col} Distribution by Churn Status"
    )
    
    fig.update_layout(
        xaxis_title="Customer Status",
        yaxis_title=numeric_col,
        showlegend=False,
        height=500
    )
    
    interpretation = f"Violin plot reveals the full distribution shape of {numeric_col}. Wider sections = more customers at that value."
    
    return fig, interpretation

# ============================================================================
# CUSTOMER SEGMENTATION VISUALIZATIONS
# ============================================================================

def create_customer_segment_sunburst(df):
    """
    Create sunburst chart showing customer segmentation hierarchy
    
    Visualizes customers by region -> payment type -> churn status
    """
    if df is None or df.empty:
        return None, None
    
    required_cols = ['region', 'payment_type', TARGET_COL]
    if not all(col in df.columns for col in required_cols):
        return None, None
    
    # Prepare data for sunburst
    df_copy = df.copy()
    df_copy['churn_status'] = df_copy[TARGET_COL].map({0: 'Retained', 1: 'Churned'})
    
    fig = px.sunburst(
        df_copy,
        path=['region', 'payment_type', 'churn_status'],
        title="Customer Segmentation: Region → Payment Type → Churn Status",
        color='churn_status',
        color_discrete_map={'Retained': '#4ECDC4', 'Churned': '#FF6B6B'}
    )
    
    fig.update_layout(height=600)
    
    interpretation = "Sunburst shows customer hierarchy. Click segments to drill down. Larger segments = more customers."
    
    return fig, interpretation

def create_treemap_analysis(df):
    """
    Create treemap for hierarchical customer value analysis
    
    Shows customer distribution and value across segments
    """
    if df is None or df.empty:
        return None, None
    
    required_cols = ['region', 'payment_type', TARGET_COL]
    if not all(col in df.columns for col in required_cols):
        return None, None
    
    # Aggregate data
    df_copy = df.copy()
    df_copy['churn_status'] = df_copy[TARGET_COL].map({0: 'Retained', 1: 'Churned'})
    
    agg_df = df_copy.groupby(['region', 'payment_type', 'churn_status']).agg({
        'customer_id': 'count',
        'avg_order_value': 'mean'
    }).reset_index()
    
    agg_df.columns = ['region', 'payment_type', 'churn_status', 'count', 'avg_value']
    
    fig = px.treemap(
        agg_df,
        path=['region', 'payment_type', 'churn_status'],
        values='count',
        color='avg_value',
        color_continuous_scale='RdYlGn',
        title="Customer Treemap: Size = Count, Color = Avg Order Value"
    )
    
    fig.update_layout(height=600)
    
    interpretation = "Treemap size = customer count, color = average value. Green = high value, red = low value. Focus on large red boxes!"
    
    return fig, interpretation

# ============================================================================
# MULTI-DIMENSIONAL ANALYSIS
# ============================================================================

def create_parallel_coordinates(df):
    """
    Create parallel coordinates plot for multi-dimensional analysis
    
    Shows relationships across multiple numeric features simultaneously
    """
    if df is None or df.empty:
        return None, None
    
    # Select key numeric columns
    plot_cols = ['age', 'total_orders', 'avg_order_value', 'loyalty_score', 'complaints', TARGET_COL]
    available_cols = [col for col in plot_cols if col in df.columns]
    
    if len(available_cols) < 3:
        return None, None
    
    # Sample data if too large
    plot_df = df[available_cols].copy()
    if len(plot_df) > 1000:
        plot_df = plot_df.sample(1000, random_state=42)
    
    # Normalize numeric columns for better visualization
    for col in available_cols:
        if col != TARGET_COL:
            plot_df[col] = (plot_df[col] - plot_df[col].min()) / (plot_df[col].max() - plot_df[col].min())
    
    fig = px.parallel_coordinates(
        plot_df,
        color=TARGET_COL,
        color_continuous_scale=['#4ECDC4', '#FF6B6B'],
        title="Parallel Coordinates: Multi-Dimensional Customer Analysis"
    )
    
    fig.update_layout(height=600)
    
    interpretation = "Each line = one customer. Red lines = churned. Look for patterns where red lines cluster together!"
    
    return fig, interpretation

def create_scatter_matrix(df):
    """
    Create scatter matrix for pairwise feature relationships
    
    Shows correlations and patterns across multiple dimensions
    """
    if df is None or df.empty:
        return None, None
    
    # Select key numeric columns
    plot_cols = ['age', 'total_orders', 'avg_order_value', 'loyalty_score', 'days_since_last_purchase']
    available_cols = [col for col in plot_cols if col in df.columns]
    
    if len(available_cols) < 3 or TARGET_COL not in df.columns:
        return None, None
    
    # Sample data if too large
    plot_df = df[available_cols + [TARGET_COL]].copy()
    if len(plot_df) > 500:
        plot_df = plot_df.sample(500, random_state=42)
    
    plot_df['churn_status'] = plot_df[TARGET_COL].map({0: 'Retained', 1: 'Churned'})
    
    fig = px.scatter_matrix(
        plot_df,
        dimensions=available_cols,
        color='churn_status',
        color_discrete_map={'Retained': '#4ECDC4', 'Churned': '#FF6B6B'},
        title="Scatter Matrix: Pairwise Feature Relationships"
    )
    
    fig.update_layout(height=800, width=800)
    
    interpretation = "Scatter matrix shows all feature pairs. Look for clear separation between blue (retained) and red (churned) points!"
    
    return fig, interpretation

# ============================================================================
# TIME-BASED ANALYSIS
# ============================================================================

def create_cohort_analysis(df):
    """
    Create cohort analysis based on tenure
    
    Shows churn patterns across customer lifecycle stages
    """
    if df is None or df.empty or 'tenure_months' not in df.columns or TARGET_COL not in df.columns:
        return None, None
    
    # Create tenure cohorts
    bins = [0, 3, 6, 12, 24, 36, float('inf')]
    labels = ['0-3m', '3-6m', '6-12m', '1-2y', '2-3y', '3y+']
    
    df_copy = df.copy()
    df_copy['cohort'] = pd.cut(df_copy['tenure_months'], bins=bins, labels=labels, right=False)
    
    # Calculate metrics by cohort
    cohort_stats = df_copy.groupby('cohort').agg({
        TARGET_COL: ['mean', 'count'],
        'avg_order_value': 'mean',
        'loyalty_score': 'mean'
    }).reset_index()
    
    cohort_stats.columns = ['cohort', 'churn_rate', 'count', 'avg_value', 'avg_loyalty']
    cohort_stats['churn_rate'] = cohort_stats['churn_rate'] * 100
    
    # Create multi-trace plot
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Churn Rate by Cohort", "Customer Count by Cohort"),
        specs=[[{"secondary_y": False}, {"type": "bar"}]]
    )
    
    # Churn rate line
    fig.add_trace(
        go.Scatter(
            x=cohort_stats['cohort'],
            y=cohort_stats['churn_rate'],
            mode='lines+markers',
            name='Churn Rate',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=10)
        ),
        row=1, col=1
    )
    
    # Customer count bars
    fig.add_trace(
        go.Bar(
            x=cohort_stats['cohort'],
            y=cohort_stats['count'],
            name='Customer Count',
            marker_color='#4ECDC4'
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Tenure Cohort", row=1, col=1)
    fig.update_xaxes(title_text="Tenure Cohort", row=1, col=2)
    fig.update_yaxes(title_text="Churn Rate (%)", row=1, col=1)
    fig.update_yaxes(title_text="Customer Count", row=1, col=2)
    
    fig.update_layout(
        title_text="Cohort Analysis: Churn Patterns Across Customer Lifecycle",
        height=500,
        showlegend=True
    )
    
    # Find critical cohort
    max_churn_cohort = cohort_stats.loc[cohort_stats['churn_rate'].idxmax()]
    interpretation = f"Critical period: {max_churn_cohort['cohort']} cohort has {max_churn_cohort['churn_rate']:.1f}% churn rate. Focus retention efforts here!"
    
    return fig, interpretation

# ============================================================================
# FEATURE IMPORTANCE VISUALIZATION
# ============================================================================

def create_feature_importance_chart(df):
    """
    Create feature importance chart based on correlation with churn
    
    Shows which features are most predictive of churn
    """
    if df is None or df.empty or TARGET_COL not in df.columns:
        return None, None
    
    # Calculate correlations with churn
    numeric_cols = [col for col in NUMERIC_COLS if col in df.columns]
    
    if len(numeric_cols) == 0:
        return None, None
    
    correlations = []
    for col in numeric_cols:
        corr = df[col].corr(df[TARGET_COL])
        correlations.append({
            'feature': col,
            'correlation': abs(corr),
            'direction': 'Positive' if corr > 0 else 'Negative',
            'raw_corr': corr
        })
    
    corr_df = pd.DataFrame(correlations).sort_values('correlation', ascending=True)
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    colors = ['#FF6B6B' if x > 0 else '#4ECDC4' for x in corr_df['raw_corr']]
    
    fig.add_trace(go.Bar(
        y=corr_df['feature'],
        x=corr_df['raw_corr'],
        orientation='h',
        marker_color=colors,
        text=corr_df['raw_corr'].apply(lambda x: f"{x:.3f}"),
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Feature Importance: Correlation with Churn",
        xaxis_title="Correlation Coefficient",
        yaxis_title="Feature",
        height=500,
        xaxis=dict(range=[-1, 1])
    )
    
    # Interpretation
    top_feature = corr_df.iloc[-1]
    interpretation = f"{top_feature['feature']} is the strongest predictor (correlation: {top_feature['raw_corr']:.3f}). Red = increases churn, blue = decreases churn."
    
    return fig, interpretation

# ============================================================================
# INTERACTIVE DRILL-DOWN ANALYSIS
# ============================================================================

def create_interactive_churn_explorer(df):
    """
    Create interactive explorer with multiple filters and dimensions
    
    Allows dynamic exploration of churn patterns
    """
    if df is None or df.empty:
        return None, None
    
    required_cols = ['region', 'payment_type', 'avg_order_value', TARGET_COL]
    if not all(col in df.columns for col in required_cols):
        return None, None
    
    df_copy = df.copy()
    df_copy['churn_status'] = df_copy[TARGET_COL].map({0: 'Retained', 1: 'Churned'})
    
    # Create bubble chart
    agg_df = df_copy.groupby(['region', 'payment_type', 'churn_status']).agg({
        'customer_id': 'count',
        'avg_order_value': 'mean',
        'loyalty_score': 'mean'
    }).reset_index()
    
    agg_df.columns = ['region', 'payment_type', 'churn_status', 'count', 'avg_value', 'avg_loyalty']
    
    fig = px.scatter(
        agg_df,
        x='avg_value',
        y='avg_loyalty',
        size='count',
        color='churn_status',
        facet_col='region',
        facet_row='payment_type',
        color_discrete_map={'Retained': '#4ECDC4', 'Churned': '#FF6B6B'},
        title="Interactive Churn Explorer: Value vs Loyalty by Segment",
        hover_data=['count']
    )
    
    fig.update_layout(height=800)
    
    interpretation = "Bubble size = customer count. Explore different segments by region and payment type. Red bubbles = churn risk areas!"
    
    return fig, interpretation

# ============================================================================
# COMPREHENSIVE EDA REPORT GENERATOR
# ============================================================================

def generate_comprehensive_eda_report(df):
    """
    Generate comprehensive EDA report with all visualizations
    
    Returns list of all plots with titles and interpretations
    """
    if df is None or df.empty:
        return []
    
    plots = []
    
    # KPI Dashboard
    kpi_fig, kpi_interp = create_kpi_dashboard(df)
    if kpi_fig:
        plots.append({
            "title": "📊 KPI Dashboard",
            "plot": kpi_fig,
            "interpretation": kpi_interp,
            "category": "overview"
        })
    
    # Churn rate donut
    churn_donut, churn_interp = create_churn_donut(df)
    if churn_donut:
        plots.append({
            "title": "🎯 Overall Churn Rate",
            "plot": churn_donut,
            "interpretation": churn_interp,
            "category": "overview"
        })
    
    # Feature importance
    feat_imp_fig, feat_imp_interp = create_feature_importance_chart(df)
    if feat_imp_fig:
        plots.append({
            "title": "⭐ Feature Importance",
            "plot": feat_imp_fig,
            "interpretation": feat_imp_interp,
            "category": "importance"
        })
    
    # Correlation heatmap
    corr_plot, corr_interp = create_correlation_heatmap(df)
    if corr_plot:
        plots.append({
            "title": "🔥 Correlation Heatmap",
            "plot": corr_plot,
            "interpretation": corr_interp,
            "category": "correlation"
        })
    
    # Categorical analysis
    for cat_col in CATEGORICAL_COLS:
        if cat_col in df.columns:
            cat_plot, cat_interp = create_categorical_churn_plots(df, cat_col)
            if cat_plot:
                plots.append({
                    "title": f"📈 Churn by {cat_col.title()}",
                    "plot": cat_plot,
                    "interpretation": cat_interp,
                    "category": "categorical"
                })
    
    # Numeric distributions
    key_numeric = ['avg_order_value', 'loyalty_score', 'days_since_last_purchase', 'complaints']
    for num_col in key_numeric:
        if num_col in df.columns:
            # Histogram
            hist_plot, hist_interp = create_numeric_histogram(df, num_col)
            if hist_plot:
                plots.append({
                    "title": f"📊 Distribution: {num_col.replace('_', ' ').title()}",
                    "plot": hist_plot,
                    "interpretation": hist_interp,
                    "category": "distribution"
                })
            
            # Box plot
            box_plot, box_interp = create_box_plot_comparison(df, num_col)
            if box_plot:
                plots.append({
                    "title": f"📦 Box Plot: {num_col.replace('_', ' ').title()}",
                    "plot": box_plot,
                    "interpretation": box_interp,
                    "category": "distribution"
                })
    
    # Cohort analysis
    cohort_fig, cohort_interp = create_cohort_analysis(df)
    if cohort_fig:
        plots.append({
            "title": "👥 Cohort Analysis",
            "plot": cohort_fig,
            "interpretation": cohort_interp,
            "category": "cohort"
        })
    
    # Segmentation
    sunburst_fig, sunburst_interp = create_customer_segment_sunburst(df)
    if sunburst_fig:
        plots.append({
            "title": "🌞 Customer Segmentation Sunburst",
            "plot": sunburst_fig,
            "interpretation": sunburst_interp,
            "category": "segmentation"
        })
    
    treemap_fig, treemap_interp = create_treemap_analysis(df)
    if treemap_fig:
        plots.append({
            "title": "🗺️ Customer Value Treemap",
            "plot": treemap_fig,
            "interpretation": treemap_interp,
            "category": "segmentation"
        })
    
    # Multi-dimensional
    parallel_fig, parallel_interp = create_parallel_coordinates(df)
    if parallel_fig:
        plots.append({
            "title": "🔀 Parallel Coordinates",
            "plot": parallel_fig,
            "interpretation": parallel_interp,
            "category": "multidimensional"
        })
    
    # Specific patterns
    days_plot, days_interp = create_days_buckets_chart(df)
    if days_plot:
        plots.append({
            "title": "📅 Churn by Days Since Last Purchase",
            "plot": days_plot,
            "interpretation": days_interp,
            "category": "patterns"
        })
    
    tenure_plot, tenure_interp = create_tenure_churn_plot(df)
    if tenure_plot:
        plots.append({
            "title": "⏰ Churn by Tenure",
            "plot": tenure_plot,
            "interpretation": tenure_interp,
            "category": "patterns"
        })
    
    loyalty_plot, loyalty_interp = create_loyalty_complaints_plot(df)
    if loyalty_plot:
        plots.append({
            "title": "💔 Loyalty vs Complaints",
            "plot": loyalty_plot,
            "interpretation": loyalty_interp,
            "category": "patterns"
        })
    
    # Interactive explorer
    explorer_fig, explorer_interp = create_interactive_churn_explorer(df)
    if explorer_fig:
        plots.append({
            "title": "🔍 Interactive Churn Explorer",
            "plot": explorer_fig,
            "interpretation": explorer_interp,
            "category": "interactive"
        })
    
    return plots

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
