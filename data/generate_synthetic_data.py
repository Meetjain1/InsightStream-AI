"""
Generate synthetic e-commerce customer churn dataset
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path so we can import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.helpers import ensure_dir, SAMPLE_DATA_PATH

def generate_customer_id(i):
    """Generate a customer ID"""
    return f"CUST{i:06d}"

def generate_synthetic_data(n_samples=2000, seed=42):
    """
    Generate synthetic e-commerce customer churn dataset
    """
    np.random.seed(seed)
    
    # Generate customer IDs
    customer_ids = [generate_customer_id(i) for i in range(1, n_samples + 1)]
    
    # Generate age - bimodal distribution
    ages = np.concatenate([
        np.random.normal(27, 5, n_samples // 2),  # Younger customers
        np.random.normal(45, 10, n_samples - n_samples // 2)  # Older customers
    ])
    ages = np.clip(ages, 18, 80).astype(int)
    
    # Generate gender
    genders = np.random.choice(['Male', 'Female', 'Other'], n_samples, p=[0.48, 0.48, 0.04])
    
    # Generate region
    regions = np.random.choice(['Urban', 'Suburban', 'Rural'], n_samples, p=[0.45, 0.35, 0.2])
    
    # Generate total orders - correlated with age
    base_orders = np.random.poisson(5, n_samples)
    age_factor = (ages - 18) / 62  # Normalize age to 0-1 range
    total_orders = np.clip(base_orders + age_factor * 5, 1, 50).astype(int)
    # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    # Generate average order value - correlated with region
    base_aov = np.random.normal(50, 20, n_samples)
    region_factor = np.where(regions == 'Urban', 1.2,
                     np.where(regions == 'Suburban', 1.0, 0.8))
    avg_order_value = np.clip(base_aov * region_factor, 10, 200).round(2)
    
    # Generate days since last purchase - higher = more likely to churn
    days_since_last_purchase = np.random.exponential(30, n_samples).astype(int)
    days_since_last_purchase = np.clip(days_since_last_purchase, 1, 365)
    
    # Generate loyalty score (0-1)
    base_loyalty = np.random.beta(2, 2, n_samples)  # Beta distribution centered around 0.5
    # Adjust based on total orders (more orders = higher loyalty)
    order_factor = np.clip(total_orders / 20, 0, 1)
    # Adjust based on days since purchase (more days = lower loyalty)
    recency_factor = 1 - np.clip(days_since_last_purchase / 180, 0, 1)
    
    loyalty_score = np.clip(base_loyalty + 0.3 * order_factor + 0.3 * recency_factor, 0, 1).round(2)
    
    # Generate complaints
    # Higher complaint probability for lower loyalty scores
    complaint_prob = 0.3 * (1 - loyalty_score)
    complaints = np.random.binomial(3, complaint_prob)
    
    # Generate payment type
    payment_options = ['Credit Card', 'PayPal', 'Bank Transfer', 'Apple Pay']
    # Payment type probabilities vary by age
    young_probs = [0.3, 0.4, 0.1, 0.2]  # Younger customers use PayPal/Apple Pay more
    old_probs = [0.5, 0.2, 0.25, 0.05]  # Older customers use Credit Card/Bank Transfer more
    
    payment_probs = np.array([young_probs, old_probs])
    age_index = (ages >= 35).astype(int)
    
    payment_type = []
    for i in range(n_samples):
        probs = payment_probs[age_index[i]]
        payment_type.append(np.random.choice(payment_options, p=probs))
    
    # Generate tenure in months
    tenure_months = np.random.gamma(shape=2.0, scale=12, size=n_samples).astype(int)
    tenure_months = np.clip(tenure_months, 1, 60)
    
    # Generate promo user flag - correlated with lower loyalty and higher churn
    promo_user_prob = 0.4 * (1 - loyalty_score) + 0.1
    is_promo_user = np.random.binomial(1, promo_user_prob)
    
    # Generate churn label
    # Factors increasing churn:
    # 1. Low loyalty score
    # 2. Many complaints
    # 3. Many days since last purchase
    # 4. Low tenure
    # 5. Being a promo user
    # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    churn_prob = (
        0.3 * (1 - loyalty_score) +
        0.2 * (complaints / 3) +
        0.25 * (days_since_last_purchase / 180) +
        0.15 * (1 - tenure_months / 60) +
        0.1 * is_promo_user
    )
    
    # Ensure reasonable churn rate (around 20%)
    churn_prob = churn_prob * 0.4  # Scale down to get ~20% churn rate
    churn = np.random.binomial(1, churn_prob)
    
    # Create DataFrame
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'age': ages,
        'gender': genders,
        'region': regions,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'days_since_last_purchase': days_since_last_purchase,
        'loyalty_score': loyalty_score,
        'complaints': complaints,
        'payment_type': payment_type,
        'tenure_months': tenure_months,
        'is_promo_user': is_promo_user,
        'churn': churn
    })
    
    return df

if __name__ == "__main__":
    print("Generating synthetic customer churn dataset...")
    
    # Generate data
    df = generate_synthetic_data(n_samples=2000)
    
    # Print summary
    print(f"Generated {len(df)} customer records")
    print(f"Churn rate: {df['churn'].mean() * 100:.2f}%")
    # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    # Ensure directory exists
    ensure_dir(os.path.dirname(SAMPLE_DATA_PATH))
    
    # Save to CSV
    df.to_csv(SAMPLE_DATA_PATH, index=False)
    print(f"Saved dataset to {SAMPLE_DATA_PATH}")
    
    # Print some sample data
    print("\nSample data:")
    print(df.head())
    
    # Print some stats
    print("\nDataset statistics:")
    print(df.describe())
