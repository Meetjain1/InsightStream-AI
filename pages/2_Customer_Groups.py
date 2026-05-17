"""
Customer Segments # Set page config
st.set_page_config(
    page_title="Customer Groups",
    page_icon=":busts_in_silhouette:",
    layout="wide"
)amlit Page
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import utilities
from src.helpers import (
    NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, TARGET_COL, ID_COL,
    calculate_rfm_score
)
from src.data_prep import prepare_data_for_analysis
from src.sidebar_utils import render_quick_start_guide

# Set page config
st.set_page_config(
    page_title="Customer Groups",
    page_icon="�",
    layout="wide"
)

# Initialize session state if not exists
if 'data' not in st.session_state:
    st.session_state.data = None

render_quick_start_guide()

# Page title
st.title("Discover Your Customer Groups!")
st.markdown("Group your customers by their shopping habits and create powerful targeted strategies")

# Check if data is loaded
if st.session_state.data is None:
    st.warning("No data loaded. Please load data from the home page.")
    st.stop()

# Get data
df = st.session_state.data

# Make sure we have the required columns
required_cols = ['total_orders', 'avg_order_value', 'days_since_last_purchase']
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"Missing required columns for segmentation: {', '.join(missing_cols)}")
    st.stop()

# Create tabs for different analysis views
tab1, tab2, tab3 = st.tabs(["RFM Segmentation", "Value-Based Segmentation", "Behavioral Clusters"])

# RFM Segmentation Tab
with tab1:
    st.header("RFM Analysis")
    st.markdown("""
    RFM stands for Recency, Frequency, and Monetary value - a customer segmentation technique that uses 
    past purchase behavior to divide customers into groups.
    """)
    # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    # Calculate RFM scores if not already in the dataframe
    if 'rfm_score' not in df.columns:
        st.info("Calculating RFM scores for each customer...")
        
        # Calculate individual RFM scores
        rfm_scores = []
        for _, row in df.iterrows():
            rfm = calculate_rfm_score(
                row['days_since_last_purchase'],
                row['total_orders'],
                row['avg_order_value']
            )
            rfm_scores.append(rfm)
        
        # Add scores to dataframe
        df['recency_score'] = [score['recency_score'] for score in rfm_scores]
        df['frequency_score'] = [score['frequency_score'] for score in rfm_scores]
        df['monetary_score'] = [score['monetary_score'] for score in rfm_scores]
        df['rfm_score'] = [score['total_score'] for score in rfm_scores]
        
        # Create segments based on total RFM score
        conditions = [
            df['rfm_score'] >= 8,
            (df['rfm_score'] >= 6) & (df['rfm_score'] < 8),
            (df['rfm_score'] >= 4) & (df['rfm_score'] < 6),
            df['rfm_score'] < 4
        ]
        segment_names = ['Champions', 'Loyal Customers', 'Potential Loyalists', 'At Risk']
        df['segment'] = np.select(conditions, segment_names, default='Unknown')
        
        # Update the session state with new data
        st.session_state.data = df
        
        st.success("RFM analysis complete!")
    
    # Display segment distribution
    st.subheader("Customer Segment Distribution")
    
    segment_counts = df['segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    segment_counts['Percentage'] = segment_counts['Count'] / segment_counts['Count'].sum() * 100
    
    fig = px.pie(
        segment_counts, 
        values='Count', 
        names='Segment',
        color='Segment',
        color_discrete_map={
            'Champions': '#66c2a5',
            'Loyal Customers': '#fc8d62',
            'Potential Loyalists': '#8da0cb',
            'At Risk': '#e78ac3'
        },
        title="Customer Segments"
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Show segment table
    st.subheader("Segment Details")
    segment_df = segment_counts.copy()
    segment_df['Percentage'] = segment_df['Percentage'].round(1).astype(str) + '%'
    st.dataframe(segment_df, use_container_width=True)
    
    # RFM distribution per segment
    st.subheader("RFM Scores by Segment")
    
    rfm_by_segment = df.groupby('segment').agg({
        'recency_score': 'mean',
        'frequency_score': 'mean',
        'monetary_score': 'mean',
        'rfm_score': 'mean'
    }).reset_index()
    
    # Create radar chart
    fig = go.Figure()
    # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    for segment in rfm_by_segment['segment'].unique():
        segment_data = rfm_by_segment[rfm_by_segment['segment'] == segment]
        
        fig.add_trace(go.Scatterpolar(
            r=[
                segment_data['recency_score'].values[0],
                segment_data['frequency_score'].values[0],
                segment_data['monetary_score'].values[0],
                segment_data['recency_score'].values[0]  # Close the shape
            ],
            theta=['Recency', 'Frequency', 'Monetary', 'Recency'],
            fill='toself',
            name=segment
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3]
            )
        ),
        title="RFM Profile by Segment",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Segment characteristics
    st.subheader("Segment Characteristics")
    
    # Calculate average metrics by segment
    segment_metrics = df.groupby('segment').agg({
        'days_since_last_purchase': 'mean',
        'total_orders': 'mean',
        'avg_order_value': 'mean',
        TARGET_COL: 'mean',
        ID_COL: 'count'
    }).reset_index()
    # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    segment_metrics.columns = ['Segment', 'Days Since Purchase', 'Total Orders', 'Avg Order Value', 'Churn Rate', 'Count']
    segment_metrics['Churn Rate'] = (segment_metrics['Churn Rate'] * 100).round(1).astype(str) + '%'
    segment_metrics['Days Since Purchase'] = segment_metrics['Days Since Purchase'].round(0).astype(int)
    segment_metrics['Total Orders'] = segment_metrics['Total Orders'].round(1)
    segment_metrics['Avg Order Value'] = '$' + segment_metrics['Avg Order Value'].round(2).astype(str)
    
    st.dataframe(segment_metrics, use_container_width=True)
    
    # Segment strategies
    st.subheader("Recommended Strategies by Segment")
    
    strategies = {
        'Champions': [
            "Reward these valuable customers",
            "Create a loyalty program",
            "Ask for reviews and referrals",
            "Use as early adopters for new products"
        ],
        'Loyal Customers': [
            "Increase purchase frequency with limited time offers",
            "Cross-sell related products",
            "Provide exceptional service",
            "Create a community around your brand"
        ],
        'Potential Loyalists': [
            "Encourage more frequent purchases",
            "Provide incentives for larger orders",
            "Suggest popular items from their favorite categories",
            "Optimize the onboarding experience"
        ],
        'At Risk': [
            "Re-engagement campaigns",
            "Offer special discounts to encourage purchases",
            "Request feedback to identify issues",
            "Consider if retention is profitable for this segment"
        ]
    }
    
    # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    selected_segment = st.selectbox("Select segment for strategy recommendations:", segment_counts['Segment'].tolist())
    
    if selected_segment in strategies:
        st.write(f"**Recommended strategies for {selected_segment}:**")
        for strategy in strategies[selected_segment]:
            st.write(f"- {strategy}")
    
# Value-Based Segmentation Tab
with tab2:
    st.header("Value-Based Segmentation")
    st.markdown("""
    This analysis segments customers based on their monetary value and engagement level
    to help prioritize marketing and retention efforts.
    """)
    
    # Calculate value metrics if not already in the dataframe
    if 'clv' not in df.columns and 'avg_order_value' in df.columns and 'total_orders' in df.columns:
        # Simple CLV calculation (average order value * number of orders * estimated margin)
        estimated_margin = 0.3  # 30% profit margin
        df['clv'] = df['avg_order_value'] * df['total_orders'] * estimated_margin
    
    # Create engagement score and value thresholds - set default values
    high_engagement_threshold = 0.7
    low_engagement_threshold = 0.3
    high_value_threshold = 100  # Default value
    low_value_threshold = 30    # Default value
    # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    # Create value segments
    if 'value_segment' not in df.columns and 'clv' in df.columns:
        # Define thresholds for value segments
        high_value_threshold = df['clv'].quantile(0.8)
        low_value_threshold = df['clv'].quantile(0.3)
        
        # Create engagement score (based on recency and frequency)
        if 'days_since_last_purchase' in df.columns and 'total_orders' in df.columns:
            # Normalize days since purchase (lower is better)
            max_days = df['days_since_last_purchase'].max()
            df['recency_normalized'] = 1 - (df['days_since_last_purchase'] / max_days)
            
            # Normalize orders (higher is better)
            max_orders = df['total_orders'].max()
            df['frequency_normalized'] = df['total_orders'] / max_orders
            
            # Engagement score (combination of recency and frequency)
            df['engagement_score'] = (df['recency_normalized'] + df['frequency_normalized']) / 2
            
            # Define thresholds for engagement
            high_engagement_threshold = df['engagement_score'].quantile(0.7)
            low_engagement_threshold = df['engagement_score'].quantile(0.3)
            
            # Create value-engagement segments
            conditions = [
                (df['clv'] >= high_value_threshold) & (df['engagement_score'] >= high_engagement_threshold),
                (df['clv'] >= high_value_threshold) & (df['engagement_score'] < high_engagement_threshold),
                (df['clv'] < high_value_threshold) & (df['clv'] >= low_value_threshold) & (df['engagement_score'] >= high_engagement_threshold),
                (df['clv'] < high_value_threshold) & (df['clv'] >= low_value_threshold) & (df['engagement_score'] < high_engagement_threshold),
                (df['clv'] < low_value_threshold) & (df['engagement_score'] >= low_engagement_threshold),
                (df['clv'] < low_value_threshold) & (df['engagement_score'] < low_engagement_threshold)
            ]
            
            value_segments = [
                'High Value, High Engagement',
                'High Value, Low Engagement',
                'Medium Value, High Engagement',
                'Medium Value, Low Engagement',
                'Low Value, High Engagement',
                'Low Value, Low Engagement'
            ]
            
            df['value_segment'] = np.select(conditions, value_segments, default='Unknown')
            
            # Update the session state
            st.session_state.data = df
            # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    # Display value segments if available
    if 'value_segment' in df.columns:
        # Show segment distribution
        st.subheader("Value-Based Segment Distribution")
        
        value_counts = df['value_segment'].value_counts().reset_index()
        value_counts.columns = ['Segment', 'Count']
        
        fig = px.bar(
            value_counts,
            x='Segment',
            y='Count',
            color='Segment',
            title="Value-Based Customer Segments"
        )
        
        fig.update_layout(height=500, xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Create quadrant chart for customer value vs engagement
        st.subheader("Customer Value vs. Engagement")
        
        fig = px.scatter(
            df,
            x='engagement_score',
            y='clv',
            color='value_segment',
            size='total_orders',
            hover_name=ID_COL,
            hover_data=['avg_order_value', 'days_since_last_purchase', 'total_orders'],
            title="Customer Value vs. Engagement Quadrant"
        )
        
        # Add quadrant lines
        fig.add_shape(
            type="line", line=dict(dash="dash"),
            x0=low_engagement_threshold, y0=0,
            x1=low_engagement_threshold, y1=df['clv'].max() * 1.1,
            line_color="gray",
        )
        
        fig.add_shape(
            type="line", line=dict(dash="dash"),
            x0=0, y0=high_value_threshold,
            x1=1, y1=high_value_threshold,
            line_color="gray",
        )
        
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Churn rate by value segment
        if TARGET_COL in df.columns:
            st.subheader("Churn Rate by Value Segment")
            
            churn_by_value_segment = df.groupby('value_segment')[TARGET_COL].mean() * 100
            counts_by_value_segment = df.groupby('value_segment').size()
            
            churn_value_df = pd.DataFrame({
                'Segment': churn_by_value_segment.index,
                'Churn Rate (%)': churn_by_value_segment.values,
                'Count': counts_by_value_segment.values
            })
            
            # Sort by churn rate descending
            churn_value_df = churn_value_df.sort_values('Churn Rate (%)', ascending=False)
            
            fig = px.bar(
                churn_value_df,
                x='Segment',
                y='Churn Rate (%)',
                color='Churn Rate (%)',
                color_continuous_scale='RdYlGn_r',
                text=churn_value_df['Churn Rate (%)'].round(1).astype(str) + '%',
                title="Churn Rate by Value Segment"
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Add insight
            highest_segment = churn_value_df.iloc[0]['Segment']
            highest_rate = churn_value_df.iloc[0]['Churn Rate (%)']
            
            st.info(f"""
            **Key Insight:**
            - The "{highest_segment}" segment has the highest churn rate at {highest_rate:.1f}%
            - This indicates a need for specific retention strategies for this segment
            """)
    else:
        st.info("Value-based segmentation requires additional customer value data.")
        
# Behavioral Clusters Tab
with tab3:
    st.header("Behavioral Clustering")
    st.markdown("""
    This analysis uses customer behavior patterns to identify natural clusters of similar customers.
    """)
    
    # Placeholder for more advanced clustering
    st.info("""
    Behavioral clustering analysis typically requires unsupervised machine learning techniques 
    like K-means clustering. This has been removed from the simplified version.
    
    To implement behavioral clustering, you would:
    1. Select key behavioral features
    2. Standardize/normalize the data
    3. Apply clustering algorithms
    4. Interpret and name the resulting clusters
    """)
    
    # Simple behavioral grouping based on existing metrics
    st.subheader("Simple Behavioral Groupings")
    # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    # Check if we have enough behavioral data
    if all(col in df.columns for col in ['days_since_last_purchase', 'total_orders']):
        # Create simplified behavior groups
        if 'behavior_group' not in df.columns:
            # Create recency groups
            recent_threshold = df['days_since_last_purchase'].quantile(0.3)  # Most recent 30%
            inactive_threshold = df['days_since_last_purchase'].quantile(0.7)  # Least recent 30%
            
            # Create frequency groups
            high_freq_threshold = df['total_orders'].quantile(0.7)  # Top 30% by orders
            low_freq_threshold = df['total_orders'].quantile(0.3)  # Bottom 30% by orders
            
            # Define behavior groups
            conditions = [
                (df['days_since_last_purchase'] <= recent_threshold) & (df['total_orders'] >= high_freq_threshold),
                (df['days_since_last_purchase'] <= recent_threshold) & (df['total_orders'] < high_freq_threshold) & (df['total_orders'] >= low_freq_threshold),
                (df['days_since_last_purchase'] <= recent_threshold) & (df['total_orders'] < low_freq_threshold),
                (df['days_since_last_purchase'] > recent_threshold) & (df['days_since_last_purchase'] <= inactive_threshold) & (df['total_orders'] >= high_freq_threshold),
                (df['days_since_last_purchase'] > recent_threshold) & (df['days_since_last_purchase'] <= inactive_threshold) & (df['total_orders'] < high_freq_threshold),
                (df['days_since_last_purchase'] > inactive_threshold) & (df['total_orders'] >= high_freq_threshold),
                (df['days_since_last_purchase'] > inactive_threshold) & (df['total_orders'] < high_freq_threshold)
            ]
            
            behaviors = [
                'Frequent Shoppers',
                'Regular Shoppers',
                'New Customers',
                'Consistent Buyers',
                'Average Customers',
                'Former Loyalists',
                'Lapsed Customers'
            ]
            
            df['behavior_group'] = np.select(conditions, behaviors, default='Unknown')
            
            # Update session state
            st.session_state.data = df
        
        # Display behavior groups
        st.subheader("Behavioral Group Distribution")
        
        behavior_counts = df['behavior_group'].value_counts().reset_index()
        behavior_counts.columns = ['Group', 'Count']
        behavior_counts['Percentage'] = behavior_counts['Count'] / behavior_counts['Count'].sum() * 100
        
        fig = px.bar(
            behavior_counts,
            x='Group',
            y='Count',
            color='Group',
            text=behavior_counts['Count'],
            title="Customer Behavioral Groups"
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics by behavior group
        st.subheader("Metrics by Behavioral Group")
        
        behavior_metrics = df.groupby('behavior_group').agg({
            'days_since_last_purchase': 'mean',
            'total_orders': 'mean',
            'avg_order_value': 'mean' if 'avg_order_value' in df.columns else lambda x: 0,
            TARGET_COL: 'mean',
            ID_COL: 'count'
        }).reset_index()
        # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
        
        behavior_metrics.columns = ['Group', 'Days Since Purchase', 'Total Orders', 'Avg Order Value', 'Churn Rate', 'Count']
        behavior_metrics['Churn Rate'] = (behavior_metrics['Churn Rate'] * 100).round(1).astype(str) + '%'
        behavior_metrics['Days Since Purchase'] = behavior_metrics['Days Since Purchase'].round(0).astype(int)
        behavior_metrics['Total Orders'] = behavior_metrics['Total Orders'].round(1)
        behavior_metrics['Avg Order Value'] = '$' + behavior_metrics['Avg Order Value'].round(2).astype(str)
        
        st.dataframe(behavior_metrics, use_container_width=True)
        
        # Behavior group recommendations
        st.subheader("Behavioral Group Strategies")
        
        selected_group = st.selectbox("Select a behavioral group:", behavior_counts['Group'].tolist())
        
        behavior_strategies = {
            'Frequent Shoppers': [
                "Reward loyalty with exclusive perks and early access",
                "Create VIP tiers with increasing benefits",
                "Solicit product feedback and reviews",
                "Develop a referral program"
            ],
            'Regular Shoppers': [
                "Offer bundles of frequently purchased items",
                "Create a points program to increase purchase frequency",
                "Personalize recommendations based on purchase history",
                "Send timely replenishment reminders"
            ],
            'New Customers': [
                "Focus on excellent onboarding experience",
                "Provide educational content about product usage",
                "Request initial feedback to address concerns quickly",
                "Offer a second purchase incentive"
            ],
            'Consistent Buyers': [
                "Introduce subscription options for regular purchases",
                "Create bundle deals with complementary products",
                "Develop a tiered discount structure for bulk buying",
                "Personalize recommendations based on past purchases"
            ],
            'Average Customers': [
                "Offer limited-time promotions to drive engagement",
                "Create urgency with exclusive offers",
                "Recommend popular products they haven't tried",
                "Provide content showcasing product benefits"
            ],
            'Former Loyalists': [
                "Launch win-back campaigns with special incentives",
                "Request feedback to identify what changed",
                "Highlight new products or improvements since last purchase",
                "Offer a substantial discount on next purchase"
            ],
            'Lapsed Customers': [
                "Implement re-engagement email sequences",
                "Offer a special discount to return",
                "Update them on what's new since they've been gone",
                "Consider if retention efforts are worth the investment"
            ]
        }
        
        if selected_group in behavior_strategies:
            st.write(f"**Recommended strategies for {selected_group}:**")
            for strategy in behavior_strategies[selected_group]:
                st.write(f"- {strategy}")
    else:
        st.warning("Behavioral grouping requires data on purchase recency and frequency.")
