"""
EDA utilities for customer churn prediction app.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .helpers import NUMERIC_COLS, CATEGORICAL_COLS, TARGET_COL

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
