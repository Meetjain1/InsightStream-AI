"""
EDA and SQL Checks # Set page config
st.s# Page title
st.title("Data Exploration")
st.markdown("Dive into your customer data to uncover amazing insights and hidden patterns!")page_config(
    page_title="Data Exploration",
    page_icon=":mag:",
    layout="wide"
)amlit Page
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import sqlite3
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import utilities
from src.helpers import (
    SAMPLE_DATA_PATH, DB_PATH, NUMERIC_COLS, CATEGORICAL_COLS, 
    BINARY_COLS, TARGET_COL, ID_COL
)
from src.data_prep import load_csv, basic_clean, handle_missing
from src.eda_utils import create_eda_plots
from src.sql_utils import run_sql, get_churn_sql_queries

# Set page config
st.set_page_config(
    page_title="Data Exploration",
    page_icon="�",
    layout="wide"
)

# Initialize session state if not exists
if 'data' not in st.session_state:
    st.session_state.data = None
    # Try to load sample data
    if os.path.exists(SAMPLE_DATA_PATH):
        st.session_state.data = load_csv(SAMPLE_DATA_PATH)

if 'db_created' not in st.session_state:
    st.session_state.db_created = os.path.exists(DB_PATH)

# Page title
st.title("� Data Exploration")
st.markdown("Dive into your customer data to uncover amazing insights and hidden patterns!")

# Check if data is loaded
if st.session_state.data is None:
    st.warning("No data loaded. Please load data from the home page.")
    st.stop()

# Create tabs for EDA and SQL
tab1, tab2 = st.tabs(["📈 EDA Visualizations", "🔍 SQL Queries"])

# EDA Visualizations Tab
with tab1:
    st.header("Exploratory Data Analysis")
    
    # Clean data for visualization
    if 'data_clean' not in st.session_state:
        with st.spinner("Cleaning data for visualization..."):
            df_clean = basic_clean(st.session_state.data)
            df_clean = handle_missing(df_clean)
            st.session_state.data_clean = df_clean
    
    # Generate plots
    with st.spinner("Generating visualizations..."):
        eda_plots = create_eda_plots(st.session_state.data_clean)
    
    if eda_plots:
        # Data overview
        st.subheader("📋 Data Overview")
        
        # Basic stats in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            total_customers = len(st.session_state.data_clean)
            st.metric("Total Customers", f"{total_customers:,}")
        
        with col2:
            if TARGET_COL in st.session_state.data_clean.columns:
                churn_rate = st.session_state.data_clean[TARGET_COL].mean() * 100
                st.metric("Churn Rate", f"{churn_rate:.1f}%")
        
        with col3:
            if 'avg_order_value' in st.session_state.data_clean.columns:
                avg_value = st.session_state.data_clean['avg_order_value'].mean()
                st.metric("Avg Order Value", f"${avg_value:.2f}")
        
        # Display plots
        for i, plot_info in enumerate(eda_plots):
            st.subheader(plot_info["title"])
            st.plotly_chart(plot_info["plot"], use_container_width=True)
            
            # Display human interpretation
            st.info(f"💡 **Insight**: {plot_info['interpretation']}")
            
            # Add separator except for the last plot
            if i < len(eda_plots) - 1:
                st.markdown("---")
    else:
        st.error("Failed to generate EDA plots. Check your data.")

# SQL Queries Tab
with tab2:
    st.header("SQL Database Queries")
    
    if not st.session_state.db_created:
        st.warning("Database not created yet. Please save data to database from the home page.")
        
        if st.button("Create Database Now"):
            from src.sql_utils import create_db_and_table, upsert_clean_data
            
            with st.spinner("Creating database and saving data..."):
                create_db_and_table()
                result = upsert_clean_data(st.session_state.data_clean)
                
                if result:
                    st.session_state.db_created = True
                    st.success("Database created and data saved successfully!")
                else:
                    st.error("Failed to create database or save data.")
    else:
        st.success("Database is ready! Run SQL queries to analyze your data.")
        
        # Run pre-defined SQL queries
        if st.button("Run SQL Checks"):
            # Get predefined queries
            sql_queries = get_churn_sql_queries()
            
            with st.spinner("Running SQL queries..."):
                # Total customers
                st.subheader("Total Customers")
                result = run_sql(sql_queries["total_customers"])
                if result is not None:
                    st.dataframe(result, use_container_width=True)
                    total = result.iloc[0, 0]
                    st.write(f"We have {total:,} customers in the database. nice data size!")
                
                # Overall churn rate
                st.subheader("Overall Churn Rate")
                result = run_sql(sql_queries["churn_rate_overall"])
                if result is not None:
                    st.dataframe(result, use_container_width=True)
                    churn_rate = result.iloc[0, 2]
                    st.write(f"Overall churn rate is {churn_rate}%. we need to bring this down!")
                
                # Churn by region
                st.subheader("Churn Rate by Region")
                result = run_sql(sql_queries["churn_by_region"])
                if result is not None:
                    st.dataframe(result, use_container_width=True)
                    
                    # Visualize results
                    import plotly.express as px
                    fig = px.bar(result, x='region', y='churn_rate_pct',
                                 title="Churn Rate by Region",
                                 labels={'churn_rate_pct': 'Churn Rate (%)', 'region': 'Region'},
                                 color='churn_rate_pct',
                                 color_continuous_scale=['#4ECDC4', '#FFD166', '#FF6B6B'],
                                 text=result['churn_rate_pct'].round(1).astype(str) + '%')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Human insight
                    highest_region = result.iloc[0]['region']
                    highest_rate = result.iloc[0]['churn_rate_pct']
                    st.info(f"💡 **Insight**: {highest_region} region has highest churn at {highest_rate}%. need to focus here!")
                
                # Churn by payment type
                st.subheader("Churn Rate by Payment Type")
                result = run_sql(sql_queries["churn_by_payment_type"])
                if result is not None:
                    st.dataframe(result, use_container_width=True)
                    
                    # Visualize results
                    fig = px.bar(result, x='payment_type', y='churn_rate_pct',
                                 title="Churn Rate by Payment Type",
                                 labels={'churn_rate_pct': 'Churn Rate (%)', 'payment_type': 'Payment Type'},
                                 color='churn_rate_pct',
                                 color_continuous_scale=['#4ECDC4', '#FFD166', '#FF6B6B'],
                                 text=result['churn_rate_pct'].round(1).astype(str) + '%')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Human insight
                    highest_payment = result.iloc[0]['payment_type']
                    highest_rate = result.iloc[0]['churn_rate_pct']
                    st.info(f"💡 **Insight**: {highest_payment} users churn at {highest_rate}%. something about this payment type makes ppl leave!")
                
                # Average metrics by churn
                st.subheader("Average Metrics by Churn Status")
                result = run_sql(sql_queries["avg_metrics_by_churn"])
                if result is not None:
                    st.dataframe(result, use_container_width=True)
                    
                    # Human insight
                    churned_tenure = result[result['customer_status'] == 'Churned']['avg_tenure_months'].values[0]
                    retained_tenure = result[result['customer_status'] == 'Retained']['avg_tenure_months'].values[0]
                    tenure_diff = retained_tenure - churned_tenure
                    
                    churned_loyalty = result[result['customer_status'] == 'Churned']['avg_loyalty_score'].values[0]
                    retained_loyalty = result[result['customer_status'] == 'Retained']['avg_loyalty_score'].values[0]
                    
                    st.info(f"💡 **Insight**: Loyal customers stay {tenure_diff:.1f} months longer! And churned customers have {churned_loyalty:.2f} loyalty vs {retained_loyalty:.2f} for retained. big difference!")
                
                # Days since purchase buckets
                st.subheader("Churn by Days Since Last Purchase")
                result = run_sql(sql_queries["days_since_purchase_buckets"])
                if result is not None:
                    st.dataframe(result, use_container_width=True)
                    
                    # Visualize results
                    fig = px.bar(result, x='days_bucket', y='churn_rate_pct',
                                 title="Churn Rate by Days Since Last Purchase",
                                 labels={'churn_rate_pct': 'Churn Rate (%)', 'days_bucket': 'Days Since Last Purchase'},
                                 color='churn_rate_pct',
                                 color_continuous_scale=['#4ECDC4', '#FFD166', '#FF6B6B'],
                                 text=result['churn_rate_pct'].round(1).astype(str) + '%')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Human insight
                    highest_days = result.iloc[-1]['days_bucket']  # Assuming sorted
                    highest_rate = result.iloc[-1]['churn_rate_pct']
                    st.info(f"💡 **Insight**: Customers in '{highest_days}' bracket churn at {highest_rate}%. need to reach them before they go too long without buying!")
        # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
        # Custom SQL query
        st.subheader("Run Custom SQL Query")
        custom_query = st.text_area(
            "Enter SQL query:",
            height=150,
            placeholder="SELECT * FROM customers_clean LIMIT 10;"
        )
        
        if st.button("Run Custom Query"):
            if custom_query:
                with st.spinner("Running query..."):
                    result = run_sql(custom_query)
                    if result is not None:
                        st.dataframe(result, use_container_width=True)
                        st.success(f"Query returned {len(result)} rows. sql magic!")
                    else:
                        st.error("Query failed. Check your SQL syntax.")
            else:
                st.warning("Please enter a SQL query.")
# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
# Help section at the bottom
with st.expander("💡 EDA & SQL Tips"):
    st.markdown("""
    **EDA Tips:**
    - Look for features with big differences between churned and non-churned customers
    - Pay attention to days since last purchase and loyalty score - often strong predictors
    - Check if certain regions or payment methods have unusually high churn
    
    **SQL Tips:**
    - The database table is named `customers_clean`
    - Use SQL to segment customers and find patterns across different groups
    - Try analyzing churn by combinations of features (e.g., region AND payment type)
    """)
