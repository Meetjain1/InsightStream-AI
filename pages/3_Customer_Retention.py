"""
Why Do Customers Leave? Le# Set page config
st.set_page_config(
    page_title="Customer Retention",
    page_icon=":arrows_counterclockwise:",
    layout="wide"
)nd Out!

This page helps business owners understand why customers are walking away.
No complicated statistics - just clear insights about what might be driving customers to leave.

We look at things like:
- Which customer groups are leaving the most?
- What behaviors signal that someone might leave soon?
- How can you spot the warning signs earlier?

Think of it as your churn detective tool - helping you solve the mystery of the disappearing customers!
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import utilities
from src.helpers import (
    NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, TARGET_COL, ID_COL
)
from src.data_prep import prepare_data_for_analysis
from src.sql_utils import run_sql
from src.sidebar_utils import render_quick_start_guide

# Set page config
st.set_page_config(
    page_title="Customer Retention",
    page_icon="�",
    layout="wide"
)

# Initialize session state if not exists
if 'data' not in st.session_state:
    st.session_state.data = None
if 'data_processed' not in st.session_state:
    st.session_state.data_processed = False

render_quick_start_guide()

# Page title
st.title("Customer Retention Power Tools!")
st.markdown("Discover why customers leave and get powerful strategies to keep them coming back!")

# Check if data is loaded
if st.session_state.data is None:
    st.warning("No data loaded. Please load data from the home page.")
    st.stop()

# Check if churn column exists
if TARGET_COL not in st.session_state.data.columns:
    st.error(f"Churn column '{TARGET_COL}' not found in data. Cannot perform churn analysis.")
    st.stop()

# Process data if not already processed
if not st.session_state.data_processed:
    with st.spinner("Processing data for analysis..."):
        df = prepare_data_for_analysis(st.session_state.data)
        st.session_state.data = df
        st.session_state.data_processed = True
else:
    df = st.session_state.data

# Create tabs for different churn analysis views
tab1, tab2, tab3 = st.tabs(["Churn Factors", "Churn Trends", "Correlation Analysis"])

# Churn Factors Tab
with tab1:
    st.header("Key Churn Factors")
    st.markdown("Analyze which factors have the strongest relationship with customer churn.")
    
    # Calculate feature correlations with churn
    numeric_cols = [col for col in NUMERIC_COLS if col in df.columns]
    if numeric_cols:
        # Calculate correlations
        corr_with_churn = df[numeric_cols + [TARGET_COL]].corr()[TARGET_COL].drop(TARGET_COL).sort_values(ascending=False)
        
        # Display correlations
        st.subheader("Correlation with Churn")
        
        # Create correlation dataframe
        corr_df = pd.DataFrame({
            'Feature': corr_with_churn.index,
            'Correlation': corr_with_churn.values
        })
        
        # Create visualization
        import plotly.express as px
        
        fig = px.bar(
            corr_df,
            x='Correlation',
            y='Feature',
            orientation='h',
            color='Correlation',
            color_continuous_scale='RdBu_r',
            title="Feature Correlations with Churn"
        )

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insight
        top_pos = corr_df.iloc[0]['Feature']
        top_pos_corr = corr_df.iloc[0]['Correlation']
        top_neg = corr_df.iloc[-1]['Feature']
        top_neg_corr = corr_df.iloc[-1]['Correlation']
        
        st.info(f"""
        Insight: 
        - {top_pos} has the strongest positive correlation with churn ({top_pos_corr:.2f}). Higher values increase churn risk.
        - {top_neg} has the strongest negative correlation with churn ({top_neg_corr:.2f}). Higher values decrease churn risk.
        """)
    
    # Categorical features analysis
    st.subheader("Churn Rate by Categorical Features")
    
    # Select categorical features
    cat_cols = [col for col in CATEGORICAL_COLS + BINARY_COLS if col in df.columns]
    
    if cat_cols:
        # Select feature to analyze
        selected_cat = st.selectbox("Select categorical feature:", cat_cols)
        
        # Calculate churn rate by category
        churn_by_cat = df.groupby(selected_cat)[TARGET_COL].mean() * 100
        counts_by_cat = df.groupby(selected_cat).size()
        
        # Create dataframe
        cat_analysis = pd.DataFrame({
            selected_cat: churn_by_cat.index,
            'Churn Rate (%)': churn_by_cat.values,
            'Count': counts_by_cat.values
        })
        
        # Sort by churn rate
        cat_analysis = cat_analysis.sort_values('Churn Rate (%)', ascending=False)
        
        # Display as table
        st.dataframe(cat_analysis, use_container_width=True)
        
        # Create visualization
        fig = px.bar(
            cat_analysis,
            x=selected_cat,
            y='Churn Rate (%)',
            color='Churn Rate (%)',
            color_continuous_scale=['#4ECDC4', '#FFD166', '#FF6B6B'],
            text=cat_analysis['Churn Rate (%)'].round(1).astype(str) + '%',
            title=f"Churn Rate by {selected_cat}"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insight
        highest_cat = cat_analysis.iloc[0][selected_cat]
        highest_rate = cat_analysis.iloc[0]['Churn Rate (%)']
        lowest_cat = cat_analysis.iloc[-1][selected_cat]
        lowest_rate = cat_analysis.iloc[-1]['Churn Rate (%)']
        
        st.info(f"""
        Insight: 
        - {highest_cat} has the highest churn rate at {highest_rate:.1f}%
        - {lowest_cat} has the lowest churn rate at {lowest_rate:.1f}%
        - The difference of {highest_rate - lowest_rate:.1f} percentage points is significant!
        """)
    
    # Numeric feature analysis
    st.subheader("Churn by Numeric Features")
    
    # Select feature to analyze
    if numeric_cols:
        selected_num = st.selectbox("Select numeric feature:", numeric_cols)
        
        # Create visualization
        import plotly.figure_factory as ff
        
        # Create histogram grouped by churn
        churned = df[df[TARGET_COL] == 1][selected_num]
        retained = df[df[TARGET_COL] == 0][selected_num]
        
        hist_data = [retained, churned]
        group_labels = ['Retained', 'Churned']
        colors = ['#4ECDC4', '#FF6B6B']
        
        fig = ff.create_distplot(
            hist_data, 
            group_labels, 
            colors=colors,
            bin_size=(df[selected_num].max() - df[selected_num].min()) / 20,
            show_rug=False
        )
        
        fig.update_layout(
            title=f"Distribution of {selected_num} by Churn Status",
            xaxis_title=selected_num,
            yaxis_title="Density",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate stats
        churned_mean = churned.mean()
        retained_mean = retained.mean()
        diff_pct = abs(churned_mean - retained_mean) / retained_mean * 100
        
        if churned_mean > retained_mean:
            st.info(f"""
            Insight: 
            - Churned customers have {diff_pct:.1f}% higher {selected_num} on average ({churned_mean:.2f} vs {retained_mean:.2f})
            - Customers with higher {selected_num} are more likely to churn
            """)
        else:
            st.info(f"""
            Insight: 
            - Churned customers have {diff_pct:.1f}% lower {selected_num} on average ({churned_mean:.2f} vs {retained_mean:.2f})
            - Customers with lower {selected_num} are more likely to churn
            """)

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

# Churn Trends Tab
with tab2:
    st.header("Churn Trends")
    st.markdown("Analyze churn patterns over different dimensions.")
    
    # Churn by tenure buckets
    if 'tenure_bucket' in df.columns:
        st.subheader("Churn by Customer Tenure")
        
        # Calculate churn rate by tenure
        churn_by_tenure = df.groupby('tenure_bucket')[TARGET_COL].mean() * 100
        counts_by_tenure = df.groupby('tenure_bucket').size()
        
        # Create dataframe
        tenure_analysis = pd.DataFrame({
            'Tenure': churn_by_tenure.index,
            'Churn Rate (%)': churn_by_tenure.values,
            'Count': counts_by_tenure.values
        })
        
        # Sort by bucket order
        bucket_order = ['0-6 months', '7-12 months', '1-2 years', '2-3 years', '3+ years']
        tenure_analysis['Tenure'] = pd.Categorical(tenure_analysis['Tenure'], categories=bucket_order, ordered=True)
        tenure_analysis = tenure_analysis.sort_values('Tenure')
        
        # Display as table
        st.dataframe(tenure_analysis, use_container_width=True)
        
        # Create visualization
        import plotly.express as px
        
        fig = px.line(
            tenure_analysis,
            x='Tenure',
            y='Churn Rate (%)',
            markers=True,
            text=tenure_analysis['Churn Rate (%)'].round(1).astype(str) + '%',
            title="Churn Rate by Customer Tenure"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insight
        highest_tenure = tenure_analysis.loc[tenure_analysis['Churn Rate (%)'].idxmax()]['Tenure']
        highest_rate = tenure_analysis.loc[tenure_analysis['Churn Rate (%)'].idxmax()]['Churn Rate (%)']
        
        st.info(f"""
        Insight: 
        - Customers in the {highest_tenure} tenure bracket have the highest churn rate at {highest_rate:.1f}%
        - This indicates a critical period in the customer lifecycle that needs attention
        """)

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    # Churn by recency buckets
    if 'recency_bucket' in df.columns:
        st.subheader("Churn by Purchase Recency")
        
        # Calculate churn rate by recency
        churn_by_recency = df.groupby('recency_bucket')[TARGET_COL].mean() * 100
        counts_by_recency = df.groupby('recency_bucket').size()
        
        # Create dataframe
        recency_analysis = pd.DataFrame({
            'Recency': churn_by_recency.index,
            'Churn Rate (%)': churn_by_recency.values,
            'Count': counts_by_recency.values
        })
        
        # Sort by bucket order
        bucket_order = ['0-30 days', '31-60 days', '61-90 days', 'Over 90 days']
        recency_analysis['Recency'] = pd.Categorical(recency_analysis['Recency'], categories=bucket_order, ordered=True)
        recency_analysis = recency_analysis.sort_values('Recency')
        
        # Display as table
        st.dataframe(recency_analysis, use_container_width=True)
        
        # Create visualization
        fig = px.line(
            recency_analysis,
            x='Recency',
            y='Churn Rate (%)',
            markers=True,
            text=recency_analysis['Churn Rate (%)'].round(1).astype(str) + '%',
            title="Churn Rate by Purchase Recency"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insight
        highest_recency = recency_analysis.loc[recency_analysis['Churn Rate (%)'].idxmax()]['Recency']
        highest_rate = recency_analysis.loc[recency_analysis['Churn Rate (%)'].idxmax()]['Churn Rate (%)']
        
        st.info(f"""
        Insight: 
        - Customers who haven't purchased in {highest_recency} have the highest churn rate at {highest_rate:.1f}%
        - This indicates a critical window after which customers are much more likely to leave
        """)
    
    # Combination analysis
    st.subheader("Multi-dimensional Churn Analysis")
    
    # Select dimensions
    dimension_options = [col for col in df.columns if col not in [TARGET_COL, ID_COL] and df[col].nunique() < 10]
    
    if len(dimension_options) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            dim1 = st.selectbox("Select first dimension:", dimension_options, index=0)
        
        with col2:
            remaining_options = [col for col in dimension_options if col != dim1]
            dim2 = st.selectbox("Select second dimension:", remaining_options, index=0)
        
        # Calculate churn by dimensions
        churn_by_dims = df.groupby([dim1, dim2])[TARGET_COL].mean() * 100
        counts_by_dims = df.groupby([dim1, dim2]).size()
        
        # Create dataframe
        multi_analysis = pd.DataFrame({
            dim1: [x[0] for x in churn_by_dims.index],
            dim2: [x[1] for x in churn_by_dims.index],
            'Churn Rate (%)': churn_by_dims.values,
            'Count': counts_by_dims.values
        })
        
        # Sort by churn rate
        multi_analysis = multi_analysis.sort_values('Churn Rate (%)', ascending=False)
        
        # Display as table
        st.dataframe(multi_analysis, use_container_width=True)
        
        # Create heatmap
        import plotly.graph_objects as go
        
        # Pivot data for heatmap
        heatmap_data = df.groupby([dim1, dim2])[TARGET_COL].mean() * 100
        heatmap_data = heatmap_data.reset_index().pivot(index=dim1, columns=dim2, values=TARGET_COL)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdBu_r',
            colorbar=dict(title='Churn Rate (%)'),
            text=np.round(heatmap_data.values, 1),
            texttemplate='%{text}%',
            textfont={"size":10}
        ))

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
        
        fig.update_layout(
            title=f"Churn Rate by {dim1} and {dim2}",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insight
        if len(multi_analysis) > 0:
            highest_dim1 = multi_analysis.iloc[0][dim1]
            highest_dim2 = multi_analysis.iloc[0][dim2]
            highest_rate = multi_analysis.iloc[0]['Churn Rate (%)']
            highest_count = multi_analysis.iloc[0]['Count']
            
            lowest_dim1 = multi_analysis.iloc[-1][dim1]
            lowest_dim2 = multi_analysis.iloc[-1][dim2] 
            lowest_rate = multi_analysis.iloc[-1]['Churn Rate (%)']
            lowest_count = multi_analysis.iloc[-1]['Count']
            
            st.info(f"""
            Insight: 
            - The highest churn rate of {highest_rate:.1f}% occurs with {dim1}={highest_dim1} and {dim2}={highest_dim2} (affects {highest_count} customers)
            - The lowest churn rate of {lowest_rate:.1f}% occurs with {dim1}={lowest_dim1} and {dim2}={lowest_dim2} (affects {lowest_count} customers)
            - This combination analysis helps target specific customer segments for retention efforts
            """)

# Correlation Analysis Tab
with tab3:
    st.header("Correlation Analysis")
    st.markdown("Analyze relationships between different features and churn.")
    
    # Correlation matrix
    st.subheader("Feature Correlation Matrix")
    
    # Select features for correlation
    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and col != ID_COL]
    
    if len(numeric_cols) > 1:
        # Calculate correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        # Create heatmap
        import plotly.graph_objects as go
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu_r',
            colorbar=dict(title='Correlation'),
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size":10}
        ))
        
        fig.update_layout(
            title="Feature Correlation Matrix",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insight
        if TARGET_COL in corr_matrix.columns:
            churn_corr = corr_matrix[TARGET_COL].drop(TARGET_COL)
            top_pos = churn_corr.nlargest(1).index[0]
            top_pos_corr = churn_corr.nlargest(1).values[0]
            top_neg = churn_corr.nsmallest(1).index[0]
            top_neg_corr = churn_corr.nsmallest(1).values[0]
            
            st.info(f"""
            Insight: 
            - {top_pos} has the strongest positive correlation with churn ({top_pos_corr:.2f})
            - {top_neg} has the strongest negative correlation with churn ({top_neg_corr:.2f})
            - Also note other strong feature correlations which indicate related customer behaviors
            """)
    else:
        st.warning("Not enough numeric columns for correlation analysis.")
    
    # Pairplot for key features
    st.subheader("Pairwise Relationships")
    
    # Select features for pairplot
    if len(numeric_cols) > 2:
        # Let user select top features
        num_features = st.slider("Number of features to include:", min_value=2, max_value=min(5, len(numeric_cols)), value=3)
        
        # Always include churn if available
        if TARGET_COL in numeric_cols:
            selected_features = [TARGET_COL]
            remaining_features = [col for col in numeric_cols if col != TARGET_COL]
        else:
            selected_features = []
            remaining_features = numeric_cols
        
        # If we have correlations with churn, select the most correlated features
        if TARGET_COL in corr_matrix.columns:
            churn_corr = corr_matrix[TARGET_COL].drop(TARGET_COL)
            top_corr_features = churn_corr.abs().nlargest(num_features).index.tolist()
            selected_features.extend([f for f in top_corr_features if f not in selected_features])
        else:
            # Otherwise let user select
            feature_options = [col for col in numeric_cols if col != TARGET_COL]
            user_selected = st.multiselect("Select features to include:", feature_options, default=feature_options[:num_features])
            selected_features.extend([f for f in user_selected if f not in selected_features])
        
        # Ensure we have the right number of features
        selected_features = selected_features[:num_features]

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
        
        if len(selected_features) > 1:
            # Create scatter plot matrix
            import plotly.express as px
            
            fig = px.scatter_matrix(
                df,
                dimensions=selected_features,
                color=TARGET_COL if TARGET_COL in df.columns else None,
                color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'} if TARGET_COL in df.columns else None,
                title="Feature Relationships"
            )
            
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("""
            Tip: 
            - Look for clear separation between red (churned) and teal (retained) points
            - Features with better separation are stronger predictors of churn
            - Clusters indicate customer segments with similar behaviors
            """)
        else:
            st.warning("Please select at least 2 features for the pairwise plot.")
    else:
        st.warning("Not enough numeric columns for pairwise relationship analysis.")

# Help section at the bottom
with st.expander("Churn Analysis Tips"):
    st.markdown("""
    **How to Use Churn Analysis:**
    
    1. **Key Factors**: Focus on features with strong correlation to churn (both positive and negative)
    
    2. **Combination Analysis**: Look for specific combinations of factors that have unusually high churn rates
    
    3. **Critical Windows**: Pay attention to time-based patterns like recency and tenure windows with high churn
    
    4. **Leading Indicators**: Features with high correlation to churn can serve as early warning signs
    
    5. **Segment Targeting**: Use the multi-dimensional analysis to identify specific customer segments for 
       targeted retention campaigns
    """)
