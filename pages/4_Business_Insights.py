"""
Actionable Advice You Can Ac# Set page config
st.set_page_config(
    page_title="Business Insights",
    page_icon=":bulb:",
    layout="wide"
) Use!

This is where all the analysis turns into real-world actions you can take.
No confusing jargon or complicated strategies - just clear, practical recommendations
that can help keep your customers happy and your business growing.

We'll help you:
- Understand what the data is really saying about your customers
- Figure out which customers need attention right now
- Calculate the real dollars-and-cents impact of keeping customers around
- Create simple reports you can share with your team

It's like having a friendly business consultant in your pocket!
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import io
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import utilities
from src.helpers import (
    NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, TARGET_COL, ID_COL
)
from src.data_prep import prepare_data_for_analysis
from src.sidebar_utils import render_quick_start_guide

# Set page config
st.set_page_config(
    page_title="Business Insights",
    page_icon="�",
    layout="wide"
)

# Initialize session state if not exists
if 'data' not in st.session_state:
    st.session_state.data = None

render_quick_start_guide()

# Page title and description
st.title("Business Insights Gold Mine!")
st.markdown("Transform your customer data into money-making action plans that will revolutionize your business!")

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.


# Check if data is loaded
if st.session_state.data is None:
    st.warning("No data loaded. Please load data from the home page.")
    st.stop()

# Process data if needed
df = st.session_state.data

# --- Main Content ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Key Insights")
    
    # Overall churn rate
    churn_rate = df[TARGET_COL].mean() * 100
    
    st.metric("Overall Churn Rate", f"{churn_rate:.1f}%")
    
    # Calculate churn rates by segments if available
    if 'segment' in df.columns:
        st.write("Churn Rate by Customer Segment:")
        segment_churn = df.groupby('segment')[TARGET_COL].mean() * 100
        segment_counts = df.groupby('segment').size()
        
        for segment, rate in segment_churn.items():
            count = segment_counts[segment]
            st.metric(f"{segment} ({count} customers)", f"{rate:.1f}%")
    
    # Top churn factors
    if len(NUMERIC_COLS) > 0:
        st.write("Top Churn Indicators:")
        
        # Check which numeric columns actually exist in the dataframe
        available_numeric_cols = [col for col in NUMERIC_COLS if col in df.columns]
        
        if available_numeric_cols and TARGET_COL in df.columns:
            try:
                # Calculate correlations with churn
                corrs = df[available_numeric_cols + [TARGET_COL]].corr()[TARGET_COL].drop(TARGET_COL)
                top_corrs = corrs.abs().sort_values(ascending=False).head(3)
                
                for feature in top_corrs.index:
                    correlation = corrs[feature]
                    direction = "increases" if correlation > 0 else "decreases"
                    st.write(f"- Higher **{feature}** {direction} churn risk ({correlation:.2f})")
            except Exception:
                st.info("Insufficient data to calculate correlation indicators.")
        else:
            st.info("Insufficient columns to calculate churn indicators.")

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

with col2:
    st.subheader("Recommended Actions")
    
    # Basic recommendations based on churn rate
    if churn_rate > 20:
        st.error("Your churn rate is significantly high!")
        st.write("""
        **Immediate actions recommended:**
        1. Implement a customer retention program
        2. Review pricing and value proposition
        3. Improve customer onboarding process
        """)
    elif churn_rate > 10:
        st.warning("Your churn rate is moderately high")
        st.write("""
        **Recommended actions:**
        1. Implement targeted retention offers
        2. Improve customer support response times
        3. Analyze key friction points in customer journey
        """)
    else:
        st.success("Your churn rate is relatively low")
        st.write("""
        **Recommended actions:**
        1. Focus on upselling loyal customers
        2. Implement referral programs
        3. Continue monitoring satisfaction metrics
        """)

# Segment-specific recommendations
st.header("Segment-Specific Recommendations")

if 'segment' in df.columns:
    # Calculate churn rates and value by segment
    segment_analysis = df.groupby('segment').agg({
        TARGET_COL: 'mean',
        'avg_order_value': 'mean' if 'avg_order_value' in df.columns else lambda x: 0,
        'total_orders': 'mean' if 'total_orders' in df.columns else lambda x: 0,
    }).reset_index()
    
    # Add count column separately
    segment_counts = df.groupby('segment').size().reset_index(name='Count')
    segment_analysis = segment_analysis.merge(segment_counts, on='segment')
    
    segment_analysis.columns = ['Segment', 'Churn Rate', 'Avg Order Value', 'Avg Orders', 'Count']
    segment_analysis['Churn Rate'] = segment_analysis['Churn Rate'] * 100
    
    # Sort by count descending
    segment_analysis = segment_analysis.sort_values('Count', ascending=False)
    
    # Display table
    st.dataframe(segment_analysis)
    
    # Show recommendations for top segment
    if len(segment_analysis) > 0:
        top_segment = segment_analysis.iloc[0]['Segment']
        top_segment_churn = segment_analysis.iloc[0]['Churn Rate']
        
        st.subheader(f"Focus on {top_segment} Segment")
        
        if top_segment_churn > 15:
            st.write(f"""
            This segment has a {top_segment_churn:.1f}% churn rate and represents your largest customer group.
            
            **Recommended retention strategy:**
            1. Conduct satisfaction surveys to identify pain points
            2. Create loyalty rewards specific to this segment's behaviors
            3. Implement proactive outreach before typical churn periods
            """)
        else:
            st.write(f"""
            This segment has a {top_segment_churn:.1f}% churn rate and represents your largest customer group.
            
            **Recommended growth strategy:**
            1. Analyze what's working well for this segment
            2. Find lookalike customers for acquisition
            3. Test upselling and cross-selling opportunities
            """)
else:
    st.info("Customer segmentation not available. Run the Customer Segments analysis to get segment-specific recommendations.")

# Action planning section
st.header("Action Planning")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Short-term Actions (Next 30 Days)")
    st.write("""
    1. **Data Collection**
       - Ensure complete customer data capture
       - Implement regular satisfaction surveys
    
    2. **Quick Wins**
       - Reach out to high-value customers at risk
       - Fix common customer complaints
       
    3. **Analysis Refinement**
       - Segment customers more precisely
       - Identify key moments in the customer journey
    """)

with col2:
    st.subheader("Long-term Initiatives (3-6 Months)")
    st.write("""
    1. **Process Improvements**
       - Optimize onboarding process
       - Improve support response times
       
    2. **Value Enhancement**
       - Refine product/service offering
       - Review and adjust pricing strategy
       
    3. **Loyalty Program**
       - Design tiered rewards system
       - Implement early warning system for at-risk customers
    """)

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

# ROI Calculator
st.header("Retention ROI Calculator")
st.write("Estimate the return on investment for your customer retention initiatives")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Inputs")
    total_customers = st.number_input("Total customers", min_value=1, value=len(df))
    avg_customer_value = st.number_input("Average annual customer value ($)", min_value=0, value=500)
    current_churn = st.slider("Current churn rate (%)", min_value=0.0, max_value=100.0, value=float(churn_rate))
    target_churn = st.slider("Target churn rate (%)", min_value=0.0, max_value=100.0, value=max(5.0, float(churn_rate)-5.0))
    retention_cost = st.number_input("Cost per customer for retention program ($)", min_value=0, value=50)

with col2:
    st.subheader("Calculation")
    current_churned = int(total_customers * (current_churn / 100))
    target_churned = int(total_customers * (target_churn / 100))
    customers_saved = current_churned - target_churned
    revenue_saved = customers_saved * avg_customer_value
    program_cost = total_customers * retention_cost
    net_benefit = revenue_saved - program_cost
    roi = (net_benefit / program_cost * 100) if program_cost > 0 else 0
    
    st.metric("Customers retained", f"{customers_saved}")
    st.metric("Revenue protected", f"${revenue_saved:,.2f}")
    st.metric("Program cost", f"${program_cost:,.2f}")

with col3:
    st.subheader("Results")
    st.metric("Net benefit", f"${net_benefit:,.2f}")
    st.metric("ROI", f"{roi:.1f}%")
    
    if roi > 100:
        st.success("This program has excellent ROI potential!")
    elif roi > 0:
        st.info("This program has positive ROI potential.")
    else:
        st.error("This program may not be cost-effective. Consider adjusting.")

# Export section
st.header("Export Insights")

# Using CSV as the only export format
export_format = "CSV"
st.info("Export will be in CSV format. Select data types to include below.")
export_what = st.multiselect("Data to export:", ["Customer Segments", "Churn Risk Scores", "Recommendations"], 
                            help="Select one or more data types to include in your report.")

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.


if st.button("Generate Report"):
    # Create a report DataFrame with requested information
    if len(export_what) > 0:
        # Start with the basic customer ID and churn columns
        report_df = df[[ID_COL, TARGET_COL]].copy()
        
        # Add requested columns based on user selections
        if 'segment' in df.columns and "Customer Segments" in export_what:
            report_df['segment'] = df['segment']
        
        if "Churn Risk Scores" in export_what:
            # For churn risk scores, create a simple score based on available data
            if 'loyalty_score' in df.columns and 'days_since_last_purchase' in df.columns:
                # Create a risk score between 1-10 using loyalty and recency
                norm_loyalty = (df['loyalty_score'] - df['loyalty_score'].min()) / (df['loyalty_score'].max() - df['loyalty_score'].min())
                norm_recency = 1 - (df['days_since_last_purchase'] - df['days_since_last_purchase'].min()) / (df['days_since_last_purchase'].max() - df['days_since_last_purchase'].min())
                report_df['risk_score'] = 10 - ((norm_loyalty + norm_recency) / 2 * 10).round(1)
            else:
                # Fallback: use churn value as risk indicator
                report_df['risk_score'] = df[TARGET_COL] * 10
        
        # If recommendations are selected, add them as text columns
        if "Recommendations" in export_what:
            # Add generic recommendations based on churn values
            report_df['recommendation'] = np.where(
                df[TARGET_COL] == 1,
                "Reach out for win-back with personalized offer",
                "Send loyalty reward and upsell opportunity"
            )
            
            # Determine priority based on available columns
            if 'risk_score' in report_df.columns:
                # If risk score exists, use it for priority
                report_df['priority'] = np.where(
                    report_df['risk_score'] > 5,
                    "High",
                    "Normal"
                )
            else:
                # If no risk score, base priority on churn directly
                report_df['priority'] = np.where(
                    df[TARGET_COL] == 1,
                    "High",
                    "Normal"
                )
        
        # Create a buffer to download the data
        buffer = io.BytesIO()
        
        # Export as CSV
        report_df.to_csv(buffer, index=False)
        mime_type = "text/csv"
        file_ext = "csv"
        
        # Offer the file for download
        buffer.seek(0)
        st.download_button(
            label="Download Report",
            data=buffer,
            file_name=f"churn_analysis_report.{file_ext}",
            mime=mime_type
        )
    else:
        st.error("Please select at least one data category to export")
