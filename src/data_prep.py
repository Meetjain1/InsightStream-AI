"""
Data preparation functions for customer churn analysis dashboard.
"""
import pandas as pd
import numpy as np
import os
from sklearn.impute import SimpleImputer

from .helpers import (
    NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, 
    TARGET_COL, ID_COL, FEATURE_COLS,
    ensure_dir, calculate_rfm_score, get_risk_band
)

def load_csv(path):
    """Load CSV file into pandas DataFrame"""
    try:
        print(f"Loading data from {path}...")
        df = pd.read_csv(path)
        print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns. not bad!")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def basic_clean(df):
    """Basic cleaning - trim strings, fix weird values, cast dtypes, drop dupes"""
    if df is None or df.empty:
        print("No data to clean, sad :(")
        return None
    
    print("Starting basic cleaning...")
    
    # Make a copy to avoid modifying original
    df_clean = df.copy()
    
    # Check if we have the expected columns
    missing_cols = []
    expected_cols = FEATURE_COLS + [TARGET_COL, ID_COL]

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    for col in expected_cols:
        if col not in df_clean.columns:
            missing_cols.append(col)
    
    if missing_cols:
        print(f"Warning: Missing expected columns: {missing_cols}")
        print("Will continue with columns we have, fingers crossed...")
    
    # Drop duplicates
    old_shape = df_clean.shape[0]
    df_clean = df_clean.drop_duplicates()
    if old_shape > df_clean.shape[0]:
        print(f"Dropped {old_shape - df_clean.shape[0]} duplicate rows, sneaky dupes!")
    
    # Trim string columns
    for col in df_clean.select_dtypes(include=['object']).columns:
        df_clean[col] = df_clean[col].str.strip() if hasattr(df_clean[col], 'str') else df_clean[col]
    
    # Fix data types
    if ID_COL in df_clean.columns:
        df_clean[ID_COL] = df_clean[ID_COL].astype(str)
    
    for col in NUMERIC_COLS:
        if col in df_clean.columns:
            try:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            except:
                print(f"Couldn't convert {col} to numeric, weird values maybe?")
    
    for col in BINARY_COLS:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(int)
    
    if TARGET_COL in df_clean.columns:
        df_clean[TARGET_COL] = df_clean[TARGET_COL].astype(int)
    
    print(f"Basic cleaning complete! We have {df_clean.shape[0]} rows now. cool.")
    return df_clean

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

def handle_missing(df):
    """Handle missing values with simple imputations"""
    if df is None or df.empty:
        print("No data to handle missing values, bummer")
        return None
    
    print("Looking for missing values...")
    
    # Check if we have missing values
    missing_counts = df.isnull().sum()
    missing_cols = missing_counts[missing_counts > 0]
    
    if len(missing_cols) == 0:
        print("No missing values found! lucky us.")
        return df
    
    print(f"Found missing values in {len(missing_cols)} columns. gonna fix em...")
    
    # Make a copy to avoid modifying original
    df_clean = df.copy()
    
    # Impute numeric columns with median
    num_imputer = SimpleImputer(strategy='median')
    num_cols_to_impute = [col for col in NUMERIC_COLS if col in df_clean.columns and df_clean[col].isnull().sum() > 0]
    
    if num_cols_to_impute:
        print(f"Filling {len(num_cols_to_impute)} numeric columns with median values")
        df_clean[num_cols_to_impute] = num_imputer.fit_transform(df_clean[num_cols_to_impute])
    
    # Impute categorical columns with most frequent value
    cat_imputer = SimpleImputer(strategy='most_frequent')
    cat_cols_to_impute = [col for col in CATEGORICAL_COLS if col in df_clean.columns and df_clean[col].isnull().sum() > 0]
    
    if cat_cols_to_impute:
        print(f"Filling {len(cat_cols_to_impute)} categorical columns with most common values")
        df_clean[cat_cols_to_impute] = cat_imputer.fit_transform(df_clean[cat_cols_to_impute])
    
    # Binary columns (fill with 0 which is safer)
    bin_cols_to_impute = [col for col in BINARY_COLS if col in df_clean.columns and df_clean[col].isnull().sum() > 0]
    
    if bin_cols_to_impute:
        print(f"Filling {len(bin_cols_to_impute)} binary columns with 0s")
        for col in bin_cols_to_impute:
            df_clean[col] = df_clean[col].fillna(0)
    
    # Check if we've resolved all missing values
    remaining_missing = df_clean.isnull().sum().sum()
    if remaining_missing > 0:
        print(f"Warning: Still have {remaining_missing} missing values. thats weird :/")
    else:
        print("All missing values handled! nice and clean now.")
    
    return df_clean

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

def add_derived_features(df):
    """Add derived features for analysis"""
    if df is None or df.empty:
        print("No data to add derived features to")
        return df
    
    df_derived = df.copy()
    
    # Calculate risk band
    if TARGET_COL in df_derived.columns:
        df_derived['risk_band'] = df_derived[TARGET_COL].apply(get_risk_band)
    
    # Create RFM segments if we have the necessary columns
    required_cols = ['days_since_last_purchase', 'total_orders', 'avg_order_value']
    if all(col in df_derived.columns for col in required_cols):
        print("Adding RFM scores and segments...")
        
        # Apply RFM scoring function
        rfm_scores = df_derived.apply(
            lambda row: calculate_rfm_score(
                row['days_since_last_purchase'], 
                row['total_orders'], 
                row['avg_order_value']
            ), 
            axis=1
        )
        
        # Extract individual scores
        df_derived['recency_score'] = rfm_scores.apply(lambda x: x['recency_score'])
        df_derived['frequency_score'] = rfm_scores.apply(lambda x: x['frequency_score'])
        df_derived['monetary_score'] = rfm_scores.apply(lambda x: x['monetary_score'])
        df_derived['rfm_score'] = rfm_scores.apply(lambda x: x['total_score'])
        
        # Create RFM segments
        df_derived['customer_segment'] = pd.cut(
            df_derived['rfm_score'],
            bins=[0, 3, 6, 9],
            labels=['Low Value', 'Medium Value', 'High Value']
        )
        
        print("Added RFM scores and customer segments!")
    
    # Add tenure buckets
    if 'tenure_months' in df_derived.columns:
        df_derived['tenure_bucket'] = pd.cut(
            df_derived['tenure_months'],
            bins=[0, 6, 12, 24, 36, float('inf')],
            labels=['0-6 months', '7-12 months', '1-2 years', '2-3 years', '3+ years'],
            right=False
        )
    
    # Add days since purchase buckets
    if 'days_since_last_purchase' in df_derived.columns:
        df_derived['recency_bucket'] = pd.cut(
            df_derived['days_since_last_purchase'],
            bins=[0, 30, 60, 90, float('inf')],
            labels=['0-30 days', '31-60 days', '61-90 days', 'Over 90 days'],
            right=False
        )
    
    return df_derived

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

def prepare_data_for_analysis(df):
    """Run full data preparation pipeline for analysis"""
    if df is None or df.empty:
        print("No data to prepare")
        return None
    
    # Clean data
    df_clean = basic_clean(df)
    
    # Handle missing values
    df_clean = handle_missing(df_clean)
    
    # Add derived features
    df_clean = add_derived_features(df_clean)
    
    return df_clean
