"""
SQL utilities for business analysis dashboard.
"""
import os
import pandas as pd
from sqlalchemy import create_engine, text
import sqlite3
from typing import Optional, List, Dict, Any, Tuple

from .helpers import DB_PATH, ensure_dir

def create_db_and_table():
    """
    Create SQLite database and customers_clean table
    """
    try:
        # Make sure the directory exists
        ensure_dir(os.path.dirname(DB_PATH))
        
        # Create engine
        engine = create_engine(f"sqlite:///{DB_PATH}")
        
        # Create the table with the schema
        create_table_query = """
        CREATE TABLE IF NOT EXISTS customers_clean (
            customer_id TEXT PRIMARY KEY,
            age INTEGER,
            gender TEXT,
            region TEXT,
            total_orders INTEGER,
            avg_order_value REAL,
            days_since_last_purchase INTEGER,
            loyalty_score REAL,
            complaints INTEGER,
            payment_type TEXT,
            tenure_months INTEGER,
            is_promo_user INTEGER,
            churn INTEGER
        );
        """
        
        with engine.connect() as conn:
            conn.execute(text(create_table_query))
            conn.commit()
        
        print(f"Created database at {DB_PATH} with customers_clean table. nice!")
        return True
    
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def upsert_clean_data(df):
    """
    Insert or update data into customers_clean table
    """
    if df is None or df.empty:
        print("No data to insert, nothing to do :(")
        return False
    
    try:
        # Create the database and table if they don't exist
        create_db_and_table()
        
        # Create engine
        engine = create_engine(f"sqlite:///{DB_PATH}")
        
        # Insert data with "replace" method (SQLite's upsert)
        df.to_sql("customers_clean", engine, if_exists="replace", index=False)
        
        # Get row count to confirm
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM customers_clean"))
            count = result.scalar()
        
        print(f"Successfully saved {count} rows to customers_clean table! data is safe.")
        return True
    
    except Exception as e:
        print(f"Error inserting data: {e}")
        return False

def run_sql(query):
    """
    Run SQL query and return results as DataFrame
    """
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. need to create it first!")
        return None
    
    try:
        # Create engine
        engine = create_engine(f"sqlite:///{DB_PATH}")
        
        # Execute query
        with engine.connect() as conn:
            result = pd.read_sql_query(query, conn)
        
        print(f"Query returned {result.shape[0]} rows. sql magic worked!")
        return result
    
    except Exception as e:
        print(f"Error running query: {e}")
        return None

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

def get_churn_sql_queries():
    """
    Return a dictionary of SQL queries for churn analysis
    """
    return {
        "total_customers": """
            SELECT COUNT(*) AS total_customers 
            FROM customers_clean;
        """,
        
        "churn_rate_overall": """
            SELECT 
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
            FROM customers_clean;
        """,
        
        "churn_by_region": """
            SELECT 
                region,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
            FROM customers_clean
            GROUP BY region
            ORDER BY churn_rate_pct DESC;
        """,
        
        "churn_by_payment_type": """
            SELECT 
                payment_type,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
            FROM customers_clean
            GROUP BY payment_type
            ORDER BY churn_rate_pct DESC;
        """,
        
        "avg_metrics_by_churn": """
            SELECT 
                CASE WHEN churn = 1 THEN 'Churned' ELSE 'Retained' END AS customer_status,
                ROUND(AVG(tenure_months), 1) AS avg_tenure_months,
                ROUND(AVG(avg_order_value), 2) AS avg_order_value,
                ROUND(AVG(days_since_last_purchase), 1) AS avg_days_since_purchase,
                ROUND(AVG(complaints), 2) AS avg_complaints,
                ROUND(AVG(loyalty_score), 2) AS avg_loyalty_score
            FROM customers_clean
            GROUP BY churn;
        """,
        
        "days_since_purchase_buckets": """
            SELECT 
                CASE 
                    WHEN days_since_last_purchase BETWEEN 0 AND 30 THEN '0-30 days'
                    WHEN days_since_last_purchase BETWEEN 31 AND 60 THEN '31-60 days'
                    WHEN days_since_last_purchase BETWEEN 61 AND 90 THEN '61-90 days'
                    ELSE 'Over 90 days'
                END AS days_bucket,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
            FROM customers_clean
            GROUP BY days_bucket
            ORDER BY 
                CASE days_bucket
                    WHEN '0-30 days' THEN 1
                    WHEN '31-60 days' THEN 2
                    WHEN '61-90 days' THEN 3
                    ELSE 4
                END;
        """
    }

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

# Business Analysis SQL Queries
def get_business_analysis_queries():
    """
    Return a dictionary of SQL queries for business analysis
    """
    return {
        "customer_overview": """
            SELECT 
                COUNT(*) as total_customers,
                SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END) as churned_customers,
                ROUND(SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate,
                ROUND(AVG(tenure_months), 1) as avg_tenure_months,
                ROUND(AVG(total_orders), 1) as avg_orders_per_customer,
                ROUND(AVG(avg_order_value), 2) as avg_order_value
            FROM customers_clean;
        """,
        
        "customer_segments": """
            WITH customer_segments AS (
                SELECT 
                    *,
                    CASE 
                        WHEN tenure_months < 6 THEN 'New (0-6 months)'
                        WHEN tenure_months BETWEEN 6 AND 12 THEN 'Recent (6-12 months)'
                        WHEN tenure_months BETWEEN 13 AND 24 THEN 'Established (1-2 years)'
                        ELSE 'Loyal (2+ years)'
                    END AS tenure_segment,
                    CASE 
                        WHEN days_since_last_purchase BETWEEN 0 AND 30 THEN 'Active (0-30 days)'
                        WHEN days_since_last_purchase BETWEEN 31 AND 90 THEN 'Recent (31-90 days)'
                        WHEN days_since_last_purchase BETWEEN 91 AND 180 THEN 'Lapsed (91-180 days)'
                        ELSE 'Inactive (180+ days)'
                    END AS recency_segment,
                    CASE 
                        WHEN total_orders >= 10 AND avg_order_value >= 50 THEN 'High Value'
                        WHEN total_orders >= 10 THEN 'High Frequency'
                        WHEN avg_order_value >= 50 THEN 'Big Spender'
                        ELSE 'Standard'
                    END AS value_segment
                FROM customers_clean
            )
            
            SELECT 
                tenure_segment,
                recency_segment,
                value_segment,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct
            FROM customer_segments
            GROUP BY tenure_segment, recency_segment, value_segment
            HAVING COUNT(*) >= 5
            ORDER BY churn_rate_pct DESC;
        """,
        
        "rfm_analysis": """
            WITH rfm_scores AS (
                SELECT 
                    *,
                    CASE 
                        WHEN days_since_last_purchase BETWEEN 0 AND 30 THEN 5
                        WHEN days_since_last_purchase BETWEEN 31 AND 60 THEN 4
                        WHEN days_since_last_purchase BETWEEN 61 AND 90 THEN 3
                        WHEN days_since_last_purchase BETWEEN 91 AND 180 THEN 2
                        ELSE 1
                    END AS recency_score,
                    CASE 
                        WHEN total_orders >= 15 THEN 5
                        WHEN total_orders BETWEEN 10 AND 14 THEN 4
                        WHEN total_orders BETWEEN 5 AND 9 THEN 3
                        WHEN total_orders BETWEEN 2 AND 4 THEN 2
                        ELSE 1
                    END AS frequency_score,
                    CASE 
                        WHEN avg_order_value >= 100 THEN 5
                        WHEN avg_order_value BETWEEN 75 AND 99.99 THEN 4
                        WHEN avg_order_value BETWEEN 50 AND 74.99 THEN 3
                        WHEN avg_order_value BETWEEN 25 AND 49.99 THEN 2
                        ELSE 1
                    END AS monetary_score
                FROM customers_clean
            ),
            rfm_segments AS (
                SELECT 
                    *,
                    CASE 
                        WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'Champions'
                        WHEN recency_score >= 4 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Loyal Customers'
                        WHEN recency_score >= 3 AND frequency_score >= 1 AND monetary_score >= 2 THEN 'Potential Loyalists'
                        WHEN recency_score >= 4 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'New Customers'
                        WHEN recency_score >= 3 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'Promising'
                        WHEN recency_score <= 2 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'At Risk'
                        WHEN recency_score <= 2 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Need Attention'
                        WHEN recency_score <= 2 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'Hibernating'
                        WHEN recency_score <= 1 AND frequency_score <= 1 AND monetary_score <= 1 THEN 'Lost'
                        ELSE 'Others'
                    END AS rfm_segment
                FROM rfm_scores
            )
            
            SELECT 
                rfm_segment,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
                ROUND(AVG(tenure_months), 1) AS avg_tenure_months,
                ROUND(AVG(total_orders), 1) AS avg_orders,
                ROUND(AVG(avg_order_value), 2) AS avg_order_value,
                ROUND(AVG(days_since_last_purchase), 1) AS avg_days_since_purchase
            FROM rfm_segments
            GROUP BY rfm_segment
            ORDER BY churn_rate_pct DESC;
        """,
        
        "purchase_patterns": """
            SELECT 
                CASE 
                    WHEN total_orders BETWEEN 1 AND 2 THEN '1-2 orders'
                    WHEN total_orders BETWEEN 3 AND 5 THEN '3-5 orders'
                    WHEN total_orders BETWEEN 6 AND 10 THEN '6-10 orders'
                    WHEN total_orders > 10 THEN '10+ orders'
                    ELSE 'No orders'
                END AS order_frequency,
                CASE 
                    WHEN avg_order_value < 25 THEN 'Under $25'
                    WHEN avg_order_value BETWEEN 25 AND 49.99 THEN '$25-$50'
                    WHEN avg_order_value BETWEEN 50 AND 99.99 THEN '$50-$100'
                    ELSE 'Over $100'
                END AS order_value_bracket,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct
            FROM customers_clean
            GROUP BY order_frequency, order_value_bracket
            ORDER BY churn_rate_pct DESC;
        """,
        
        "demographic_analysis": """
            SELECT 
                gender,
                CASE 
                    WHEN age < 25 THEN 'Under 25'
                    WHEN age BETWEEN 25 AND 34 THEN '25-34'
                    WHEN age BETWEEN 35 AND 44 THEN '35-44'
                    WHEN age BETWEEN 45 AND 54 THEN '45-54'
                    WHEN age BETWEEN 55 AND 64 THEN '55-64'
                    ELSE '65+'
                END AS age_group,
                region,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct
            FROM customers_clean
            GROUP BY gender, age_group, region
            HAVING COUNT(*) >= 5
            ORDER BY churn_rate_pct DESC;
        """,
        
        "loyalty_analysis": """
            SELECT 
                CASE 
                    WHEN loyalty_score < 2 THEN 'Very Low (0-1.9)'
                    WHEN loyalty_score BETWEEN 2 AND 3.9 THEN 'Low (2-3.9)'
                    WHEN loyalty_score BETWEEN 4 AND 5.9 THEN 'Medium (4-5.9)'
                    WHEN loyalty_score BETWEEN 6 AND 7.9 THEN 'High (6-7.9)'
                    ELSE 'Very High (8-10)'
                END AS loyalty_bracket,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
                ROUND(AVG(tenure_months), 1) AS avg_tenure_months,
                ROUND(AVG(total_orders), 1) AS avg_orders,
                ROUND(AVG(avg_order_value), 2) AS avg_order_value
            FROM customers_clean
            GROUP BY loyalty_bracket
            ORDER BY CASE 
                    WHEN loyalty_bracket = 'Very Low (0-1.9)' THEN 1
                    WHEN loyalty_bracket = 'Low (2-3.9)' THEN 2
                    WHEN loyalty_bracket = 'Medium (4-5.9)' THEN 3
                    WHEN loyalty_bracket = 'High (6-7.9)' THEN 4
                    ELSE 5
                END;
        """,
        
        "complaints_impact": """
            SELECT 
                CASE 
                    WHEN complaints = 0 THEN 'No Complaints'
                    WHEN complaints = 1 THEN '1 Complaint'
                    WHEN complaints = 2 THEN '2 Complaints'
                    ELSE '3+ Complaints'
                END AS complaint_group,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct
            FROM customers_clean
            GROUP BY complaint_group
            ORDER BY CASE 
                    WHEN complaint_group = 'No Complaints' THEN 1
                    WHEN complaint_group = '1 Complaint' THEN 2
                    WHEN complaint_group = '2 Complaints' THEN 3
                    ELSE 4
                END;
        """,
        
        "promo_effectiveness": """
            SELECT 
                CASE WHEN is_promo_user = 1 THEN 'Promo User' ELSE 'Non-Promo User' END AS promo_status,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
                ROUND(AVG(tenure_months), 1) AS avg_tenure_months,
                ROUND(AVG(total_orders), 1) AS avg_orders,
                ROUND(AVG(avg_order_value), 2) AS avg_order_value
            FROM customers_clean
            GROUP BY promo_status;
        """,
        
        "high_risk_customers": """
            SELECT 
                customer_id,
                age,
                gender,
                region,
                tenure_months,
                total_orders,
                avg_order_value,
                days_since_last_purchase,
                loyalty_score,
                complaints
            FROM customers_clean
            WHERE churn = 0
                AND days_since_last_purchase > 60
                AND (
                    complaints > 0
                    OR loyalty_score < 4
                    OR (tenure_months < 6 AND total_orders < 3)
                )
            ORDER BY days_since_last_purchase DESC, loyalty_score ASC
            LIMIT 100;
        """
    }

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

def create_visualization_from_query(df, viz_type="bar", x_col=None, y_col=None, color_col=None, title=None):
    """
    Create a visualization from SQL query results
    
    Args:
        df: DataFrame with query results
        viz_type: Type of visualization (bar, line, pie, scatter)
        x_col: Column for x-axis
        y_col: Column for y-axis
        color_col: Column for color
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    import plotly.express as px
    
    if df.empty:
        return None
    
    if not x_col:
        x_col = df.columns[0]
    if not y_col:
        y_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    if not title:
        title = f"{y_col} by {x_col}"
    
    if viz_type == "bar":
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title
        )
    elif viz_type == "line":
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            markers=True,
            title=title
        )
    elif viz_type == "pie":
        fig = px.pie(
            df,
            names=x_col,
            values=y_col,
            title=title
        )
    elif viz_type == "scatter":
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title
        )
    else:
        return None
    
    return fig
