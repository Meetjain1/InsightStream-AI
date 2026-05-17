"""
Customer Business Analysis Dashboard for E-commerce

This is our main app file that ties everything together. It's like the home page
where users start their journey through the dashboard. From here, they can load data,
see key metrics, and navigate to different pages.

No fancy stuff here just the essential tools businesses need to understand their customers better.
Think of it as a Swiss Army knife for customer data!
"""
# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import utilities
from src.helpers import (
    SAMPLE_DATA_PATH, DB_PATH, 
    NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, TARGET_COL, ID_COL,
    ensure_dir
)
from src.data_prep import load_csv, prepare_data_for_analysis
from src.sql_utils import create_db_and_table, upsert_clean_data
from src.sidebar_utils import render_quick_start_guide

# Set page config
st.set_page_config(
    page_title="Business Analysis Dashboard",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'data_processed' not in st.session_state:
    st.session_state.data_processed = False
if 'db_created' not in st.session_state:
    st.session_state.db_created = os.path.exists(DB_PATH)

# App title and description
st.title("Supercharge Your Customer Strategy!")

st.markdown("""
## Unlock the Hidden Potential in Your Customer Data!

This powerful dashboard transforms raw customer information into **game-changing business insights**. 
Discover what makes your customers tick, why they stay (or leave), and how to boost your bottom line!

### What You'll Discover:
- **Reveal surprising patterns** in your customer data with eye-popping visualizations
- **Unearth valuable insights** with custom SQL queries anyone can use
- **Identify your VIP customers** and target them with laser precision
- **Spot at-risk customers** before they leave and win them back
- **Get brilliant, actionable ideas** to skyrocket your retention rates

**Get started now!** Load your data or try our sample dataset below.
""")

# Sidebar with data options
with st.sidebar:
    st.header("Fire Up Your Analysis!")
    
    # Load sample data button
    if st.button("Load Amazing Sample Data!"):
        # Check if sample data exists
        if os.path.exists(SAMPLE_DATA_PATH):
            with st.spinner("Loading sample data..."):
                df = load_csv(SAMPLE_DATA_PATH)
                if df is not None and not df.empty:
                    st.session_state.data = df
                    st.success(f"Loaded {len(df)} sample records! Now you can explore")
                else:
                    st.error("Failed to load sample data")
        else:
            # Try to generate sample data
            st.info("Sample data not found. Generating synthetic data...")
            try:
                # Run the data generation script
                import subprocess
                result = subprocess.run(["python", "data/generate_synthetic_data.py"], 
                                        capture_output=True, text=True)
                
                if os.path.exists(SAMPLE_DATA_PATH):
                    df = load_csv(SAMPLE_DATA_PATH)
                    if df is not None and not df.empty:
                        st.session_state.data = df
                        st.success(f"Generated and loaded {len(df)} sample records!")
                    else:
                        st.error("Failed to load generated data")
                else:
                    st.error("Failed to generate sample data")
                    st.code(result.stderr)
            except Exception as e:
                st.error(f"Error generating sample data: {str(e)}")
    
    # Upload own data
    st.subheader("Or Upload Your Own Fantastic Data!")
    uploaded_file = st.file_uploader("Drop your CSV file here and let's make magic!", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Basic validation
            required_cols = [ID_COL, TARGET_COL]
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
                st.info(f"Required columns: {', '.join(required_cols)}")
            else:
                st.session_state.data = df
                st.success(f"Uploaded {len(df)} records. Ready for analysis!")
        except Exception as e:
            st.error(f"Error uploading file: {str(e)}")
    
    # Save to database button
    if st.session_state.data is not None:
        if st.button("Blast Off to Database!"):
            with st.spinner("Saving to database..."):
                # First apply data preparation steps
                processed_data = prepare_data_for_analysis(st.session_state.data)
                result = upsert_clean_data(processed_data)
                if result:
                    st.session_state.db_created = True
                    st.session_state.data_processed = True
                    st.success("Data saved to database! SQL queries ready to go")
                else:
                    st.error("Failed to save to database")
    
    st.markdown("---")
    render_quick_start_guide(in_sidebar=True)

    # App info
    st.markdown("---")
    st.caption("Customer Insight Revolution | v2.0.0")

# Main page content
if st.session_state.data is not None:
    # Show a data preview
    st.header("Your Amazing Data Preview")
    st.write("Behold! A sneak peek at your customer goldmine:")
    st.dataframe(st.session_state.data.head(5), use_container_width=True)
    
    # Data stats
    st.subheader("Power Metrics at a Glance!")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", f"{len(st.session_state.data):,}")
    with col2:
        churn_rate = st.session_state.data[TARGET_COL].mean() * 100
        st.metric("Churn Rate", f"{churn_rate:.1f}%")
    with col3:
        if 'avg_order_value' in st.session_state.data.columns:
            avg_order = st.session_state.data['avg_order_value'].mean()
            st.metric("Avg Order Value", f"${avg_order:.2f}")
    with col4:
        if 'tenure_months' in st.session_state.data.columns:
            avg_tenure = st.session_state.data['tenure_months'].mean()
            st.metric("Avg Customer Lifespan", f"{avg_tenure:.1f} months")
    
    st.markdown("---")
    
    # Business KPIs
    st.header("Treasure Trove of Business Insights")
    
    # Calculate important metrics
    active_customers = len(st.session_state.data[st.session_state.data[TARGET_COL] == 0])
    churn_count = len(st.session_state.data[st.session_state.data[TARGET_COL] == 1])
    
    # Customer Lifetime Value calculation (if relevant columns exist)
    if 'avg_order_value' in st.session_state.data.columns and 'tenure_months' in st.session_state.data.columns:
        # Simplified CLV calculation
        avg_monthly_revenue = st.session_state.data['avg_order_value'].mean()
        avg_lifetime = st.session_state.data['tenure_months'].mean()
        estimated_margin = 0.3  # Assuming 30% profit margin
        clv = avg_monthly_revenue * avg_lifetime * estimated_margin
    else:
        clv = None
    
    # Display metrics in cards
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.markdown("### Active Customers")
        st.markdown(f"<h2 style='text-align: center; color: #4ECDC4;'>{active_customers:,}</h2>", unsafe_allow_html=True)
        retention_rate = active_customers / len(st.session_state.data) * 100
        st.markdown(f"<p style='text-align: center;'>Retention Rate: {retention_rate:.1f}%</p>", unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown("### Churned Customers")
        st.markdown(f"<h2 style='text-align: center; color: #FF6B6B;'>{churn_count:,}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Churn Rate: {churn_rate:.1f}%</p>", unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown("### Customer Lifetime Value")
        if clv:
            st.markdown(f"<h2 style='text-align: center; color: #FFD166;'>${clv:.2f}</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Average value per customer</p>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='text-align: center; color: #FFD166;'>N/A</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Insufficient data to calculate</p>", unsafe_allow_html=True)

    st.markdown("---")

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

    # Navigation help
    st.header("Your Adventure Map")
    st.write("Embark on your data journey through these exciting destinations:")
    
    # Page descriptions with icons
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Data Exploration")
        st.write("""
        - **Uncover hidden gems** in your customer data
        - **Spot exciting trends** that others miss
        - **Create powerful SQL queries** with ease
        - **Build eye-popping visualizations** instantly
        """)
        
        st.markdown("### Customer Groups")
        st.write("""
        - **Discover your customer tribes** based on real behavior
        - **Decode buying patterns** that drive purchases
        - **Identify your VIP customers** worth pampering
        - **Unlock special insights** for each customer group
        """)
    
    with col2:
        st.markdown("### Customer Retention")
        st.write("""
        - **Discover why customers leave** (and how to make them stay!)
        - **Pinpoint loyalty patterns** across customer groups
        - **Track retention trends** with stunning visuals
        - **Connect the dots** between behavior and loyalty
        """)
        
        st.markdown("### Business Insights")
        st.write("""
        - **Transform data into money-making actions**
        - **Craft laser-targeted strategies** for each group
        - **Calculate the profit impact** of your retention efforts
        - **Generate brilliant action plans** your team will love
        """)

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

else:
    # No data loaded yet
    st.info("Ready for liftoff! Load our amazing sample data or upload your own to begin your data adventure!")
    
    # Show example of what the data should look like
    st.subheader("Example Data Format")
    
    # Create example data
    example_data = {
        'customer_id': ['CUST000123', 'CUST000456', 'CUST000789'],
        'age': [32, 45, 28],
        'gender': ['Female', 'Male', 'Female'],
        'region': ['Urban', 'Suburban', 'Rural'],
        'total_orders': [15, 4, 8],
        'avg_order_value': [75.20, 120.50, 55.30],
        'days_since_last_purchase': [12, 90, 30],
        'loyalty_score': [0.75, 0.30, 0.60],
        'complaints': [0, 2, 1],
        'payment_type': ['Credit Card', 'PayPal', 'Credit Card'],
        'tenure_months': [24, 8, 12],
        'is_promo_user': [0, 1, 0],
        'churn': [0, 1, 0]
    }
    
    example_df = pd.DataFrame(example_data)
    st.dataframe(example_df, use_container_width=True)
    
    st.markdown("""
    **Required columns:**
    - `customer_id`: Unique customer identifier
    - `churn`: Target variable (0 = retained, 1 = churned)
    
    **Recommended columns:**
    - Demographic data (age, gender, region)
    - Purchase history (total_orders, avg_order_value)
    - Engagement metrics (days_since_last_purchase, loyalty_score)
    - Other relevant features (complaints, payment_type, etc.)
    """)
# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

