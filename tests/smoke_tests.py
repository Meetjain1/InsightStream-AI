"""
Smoke tests for customer churn prediction app.
"""
import os
import sys
import unittest
import pandas as pd
import numpy as np

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.helpers import SAMPLE_DATA_PATH, BEST_MODEL_PATH
from src.data_prep import load_csv, basic_clean, handle_missing, preprocess_data, split_train_test
from src.model_train import train_model, evaluate_model, save_model
from src.predict_utils import predict_single, predict_batch

class SmokeTests(unittest.TestCase):
    """Basic smoke tests to ensure core functionality works"""
    
    def setUp(self):
        """Set up test data"""
        # Check if sample data exists, if not create minimal test data
        if os.path.exists(SAMPLE_DATA_PATH):
            self.df = load_csv(SAMPLE_DATA_PATH)
        else:
            print("Sample data not found, creating test data")
            # Create minimal test data
            data = {
                'customer_id': [f'CUST{i:06d}' for i in range(1, 101)],
                'age': np.random.randint(18, 80, 100),
                'gender': np.random.choice(['Male', 'Female', 'Other'], 100),
                'region': np.random.choice(['Urban', 'Suburban', 'Rural'], 100),
                'total_orders': np.random.randint(1, 50, 100),
                'avg_order_value': np.random.uniform(10, 200, 100),
                'days_since_last_purchase': np.random.randint(1, 365, 100),
                'loyalty_score': np.random.uniform(0, 1, 100),
                'complaints': np.random.randint(0, 4, 100),
                'payment_type': np.random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Apple Pay'], 100),
                'tenure_months': np.random.randint(1, 60, 100),
                'is_promo_user': np.random.randint(0, 2, 100),
                'churn': np.random.randint(0, 2, 100)
            }
            self.df = pd.DataFrame(data)
    
    def test_data_loading(self):
        """Test data loading function"""
        self.assertIsNotNone(self.df, "Data loading failed")
        self.assertGreater(len(self.df), 0, "Loaded dataframe is empty")
        print("✓ Data loading test passed")
        
# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    def test_data_cleaning(self):
        """Test data cleaning functions"""
        # Basic clean
        df_clean = basic_clean(self.df)
        self.assertIsNotNone(df_clean, "Basic cleaning failed")
        
        # Handle missing values
        df_clean = handle_missing(df_clean)
        self.assertIsNotNone(df_clean, "Missing value handling failed")
        
        # Check no missing values
        self.assertEqual(df_clean.isnull().sum().sum(), 0, "Still have missing values after cleaning")
        print("✓ Data cleaning test passed")
    
    def test_data_preprocessing(self):
        """Test full preprocessing pipeline"""
        # Full preprocessing
        df_processed = preprocess_data(self.df)
        self.assertIsNotNone(df_processed, "Data preprocessing failed")
        print("✓ Data preprocessing test passed")
    
    def test_train_test_split(self):
        """Test train-test split function"""
        # Clean data first
        df_clean = basic_clean(self.df)
        df_clean = handle_missing(df_clean)
        
        # Split data
        X_train, X_test, y_train, y_test = split_train_test(df_clean)
        
        self.assertIsNotNone(X_train, "Train-test split failed - X_train is None")
        self.assertIsNotNone(X_test, "Train-test split failed - X_test is None")
        self.assertIsNotNone(y_train, "Train-test split failed - y_train is None")
        self.assertIsNotNone(y_test, "Train-test split failed - y_test is None")
        
        print("✓ Train-test split test passed")
    
    def test_model_training(self):
        """Test model training with a tiny dataset"""
        # Preprocess data
        df_clean = basic_clean(self.df)
        df_clean = handle_missing(df_clean)
        
        # Split data
        X_train, X_test, y_train, y_test = split_train_test(df_clean)
        
        # Train a tiny model
        model = train_model(X_train, y_train, model_type='logistic_regression')
        
        self.assertIsNotNone(model, "Model training failed")
        print("✓ Model training test passed")
    
    def test_model_evaluation(self):
        """Test model evaluation"""
        # Preprocess data
        df_clean = basic_clean(self.df)
        df_clean = handle_missing(df_clean)
        
        # Split data
        X_train, X_test, y_train, y_test = split_train_test(df_clean)
        
        # Train a tiny model
        model = train_model(X_train, y_train, model_type='logistic_regression')
        
        # Evaluate model
        metrics, _, _ = evaluate_model(model, X_test, y_test)
        
        self.assertIsNotNone(metrics, "Model evaluation failed")
        self.assertIn('accuracy', metrics, "Accuracy not found in metrics")
        self.assertIn('roc_auc', metrics, "ROC AUC not found in metrics")
        
        print("✓ Model evaluation test passed")

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
    
    def test_model_save_load(self):
        """Test model saving and loading"""
        # Preprocess data
        df_clean = basic_clean(self.df)
        df_clean = handle_missing(df_clean)
        
        # Split data
        X_train, X_test, y_train, y_test = split_train_test(df_clean)
        
        # Train a tiny model
        model = train_model(X_train, y_train, model_type='logistic_regression')
        
        # Evaluate model
        metrics, _, _ = evaluate_model(model, X_test, y_test)
        
        # Save model
        saved = save_model(model, X_train.columns, metrics)
        self.assertTrue(saved, "Model saving failed")
        self.assertTrue(os.path.exists(BEST_MODEL_PATH), f"Model file not found at {BEST_MODEL_PATH}")
        
        print("✓ Model save/load test passed")
    
    def test_prediction(self):
        """Test prediction functions"""
        # First make sure we have a model
        if not os.path.exists(BEST_MODEL_PATH):
            # Preprocess data
            df_clean = basic_clean(self.df)
            df_clean = handle_missing(df_clean)
            
            # Split data
            X_train, X_test, y_train, y_test = split_train_test(df_clean)
            
            # Train a tiny model
            model = train_model(X_train, y_train, model_type='logistic_regression')
            
            # Save model
            save_model(model, X_train.columns)
        
        # Create a test input
        test_input = {
            'customer_id': 'CUST999999',
            'age': 35,
            'gender': 'Female',
            'region': 'Urban',
            'total_orders': 10,
            'avg_order_value': 100.0,
            'days_since_last_purchase': 30,
            'loyalty_score': 0.7,
            'complaints': 0,
            'payment_type': 'Credit Card',
            'tenure_months': 24,
            'is_promo_user': 0
        }
        
        # Test single prediction
        result = predict_single(test_input)
        
        self.assertIsNotNone(result, "Single prediction failed")
        self.assertNotIn('error', result, f"Prediction error: {result.get('error', '')}")
        self.assertIn('churn_probability', result, "Churn probability not found in result")
        
        # Check probability is between 0 and 1
        self.assertGreaterEqual(result['churn_probability'], 0, "Churn probability < 0")
        self.assertLessEqual(result['churn_probability'], 1, "Churn probability > 1")
        
        print("✓ Prediction test passed")
    
    def test_batch_prediction(self):
        """Test batch prediction function"""
        # First make sure we have a model
        if not os.path.exists(BEST_MODEL_PATH):
            # Preprocess data
            df_clean = basic_clean(self.df)
            df_clean = handle_missing(df_clean)
            
            # Split data
            X_train, X_test, y_train, y_test = split_train_test(df_clean)
            
            # Train a tiny model
            model = train_model(X_train, y_train, model_type='logistic_regression')
            
            # Save model
            save_model(model, X_train.columns)
        
        # Use a small sample of our dataframe
        test_batch = self.df.head(10)
        
        # Test batch prediction
        results_df, error = predict_batch(test_batch)
        
        self.assertIsNone(error, f"Batch prediction error: {error}")
        self.assertIsNotNone(results_df, "Batch prediction returned None")
        self.assertGreater(len(results_df), 0, "Batch prediction returned empty dataframe")
        self.assertIn('churn_probability', results_df.columns, "Churn probability not found in results")
        
        # Check all probabilities are between 0 and 1
        self.assertTrue((results_df['churn_probability'] >= 0).all(), "Some churn probabilities < 0")
        self.assertTrue((results_df['churn_probability'] <= 1).all(), "Some churn probabilities > 1")
        
        print("✓ Batch prediction test passed")

if __name__ == '__main__':
    print("Running smoke tests...")
    unittest.main()
