"""
The Helper's Toolbox - Making Life Easier!

This file has all those handy tools and settings that we use throughout the dashboard.
It's like the utility belt that keeps everything running smoothly.

No rocket science here - just practical functions that save us time and keep things consistent.
"""
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Root dir
ROOT_DIR = Path(__file__).parent.parent

# Data paths
DATA_DIR = os.path.join(ROOT_DIR, "data")
SAMPLE_DATA_PATH = os.path.join(DATA_DIR, "sample_churn.csv")
DB_PATH = os.path.join(DATA_DIR, "app.db")

# Data config
TARGET_COL = "churn"

# Feature groups
NUMERIC_COLS = [
    "age", 
    "total_orders", 
    "avg_order_value", 
    "days_since_last_purchase", 
    "loyalty_score", 
    "complaints", 
    "tenure_months"
]

CATEGORICAL_COLS = [
    "gender", 
    "region", 
    "payment_type"
]

BINARY_COLS = [
    "is_promo_user"
]

ID_COL = "customer_id"

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
# All features (excluding target and id)
FEATURE_COLS = NUMERIC_COLS + CATEGORICAL_COLS + BINARY_COLS

# Business config
COST_RETAIN = 50  # cost of retention offer
AVG_FUTURE_ORDERS = 3  # expected future orders if customer stays

# Simple helper to check if a directory exists, if not create it
def ensure_dir(directory):
    """Make sure directory exists, if not create it"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    return directory

def get_risk_band(churn_value):
    """Convert churn value to risk band based on business rules"""
    if churn_value == 1:
        return "High Risk"
    else:
        return "Low Risk"

def calculate_days_recency_score(days_since_purchase):
    """Calculate recency score based on days since last purchase"""
    if days_since_purchase <= 30:
        return 3  # Recently active
    elif days_since_purchase <= 90:
        return 2  # Active but slipping
    else:
        return 1  # Inactive

def calculate_frequency_score(total_orders):
    """Calculate frequency score based on total orders"""
    if total_orders >= 10:
        return 3  # Frequent buyer
    elif total_orders >= 5:
        return 2  # Regular buyer
    else:
        return 1  # Occasional buyer

def calculate_monetary_score(avg_order_value):
    """Calculate monetary score based on average order value"""
    if avg_order_value >= 100:
        return 3  # High value
    elif avg_order_value >= 50:
        return 2  # Medium value
    else:
        return 1  # Low value

def calculate_rfm_score(days_since_purchase, total_orders, avg_order_value):
    """Calculate RFM score for customer segmentation"""
    r_score = calculate_days_recency_score(days_since_purchase)
    f_score = calculate_frequency_score(total_orders)
    m_score = calculate_monetary_score(avg_order_value)
    
    return {
        'recency_score': r_score,
        'frequency_score': f_score,
        'monetary_score': m_score,
        'total_score': r_score + f_score + m_score
    }
