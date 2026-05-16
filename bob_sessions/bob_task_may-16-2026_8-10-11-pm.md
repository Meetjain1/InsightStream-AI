# Data Preparation Module Refactoring Design

## Executive Summary

This document outlines the comprehensive refactoring plan for the InsightStream-AI data preparation module. The goal is to transform the existing functional approach into a robust, class-based architecture that supports both analytics and ML workflows while maintaining backward compatibility.

## Current State Analysis

### Existing Implementation ([`src/data_prep.py`](../src/data_prep.py))

**Strengths:**
- ✅ Basic CSV loading functionality
- ✅ Duplicate removal
- ✅ Missing value imputation (median for numeric, mode for categorical)
- ✅ Data type casting and validation
- ✅ Derived feature engineering (RFM scores, tenure buckets)
- ✅ Integration with existing helpers and column definitions

**Gaps Identified:**
- ❌ No categorical encoding for ML models
- ❌ No numerical feature scaling
- ❌ No train/test split functionality
- ❌ No model artifact persistence (encoders/scalers)
- ❌ Limited data validation and quality reporting
- ❌ No support for different imputation strategies
- ❌ Functional approach limits extensibility
- ❌ No pipeline configuration system

### Dependencies
- **Column Definitions:** [`src/helpers.py`](../src/helpers.py) - `NUMERIC_COLS`, `CATEGORICAL_COLS`, `BINARY_COLS`, `TARGET_COL`, `ID_COL`
- **Existing Encoders:** [`models/encoders_scalers/`](../models/encoders_scalers/) - `ohe_encoder.pkl`, `num_scaler.pkl`
- **Data Source:** [`data/sample_churn.csv`](../data/sample_churn.csv) - Customer churn dataset

---

## Proposed Architecture

### Design Principles

1. **Modularity:** Each preprocessing step is encapsulated in its own class
2. **Composability:** Classes can be combined in flexible pipelines
3. **Reusability:** Components can be used independently or together
4. **Extensibility:** Easy to add new preprocessing strategies
5. **Backward Compatibility:** Existing functions remain available
6. **ML-Ready:** Full support for training and inference workflows

### Class Hierarchy

```
DataPreprocessor (Orchestrator)
├── DataLoader (CSV loading & validation)
├── DataCleaner (Missing values, duplicates, types)
├── FeatureEncoder (Categorical encoding)
├── FeatureScaler (Numerical scaling)
└── FeatureEngineer (Derived features)
```

---

## Detailed Component Design

### 1. DataLoader Class

**Purpose:** Load and validate CSV data with comprehensive error handling

**Key Features:**
- CSV file loading with encoding detection
- Schema validation against expected columns
- Data type inference and validation
- Sample size validation
- Memory-efficient loading for large files
- Support for multiple file formats (CSV, Excel, Parquet)

**Methods:**
```python
class DataLoader:
    def __init__(self, expected_columns=None, required_columns=None)
    def load_csv(self, path, **kwargs) -> pd.DataFrame
    def validate_schema(self, df) -> Dict[str, Any]
    def get_data_summary(self, df) -> Dict[str, Any]
```

**Validation Checks:**
- Missing required columns
- Unexpected columns
- Data type mismatches
- Empty dataframe
- Duplicate column names

---

### 2. DataCleaner Class

**Purpose:** Handle data quality issues (missing values, duplicates, outliers)

**Key Features:**
- Multiple imputation strategies (mean, median, mode, forward-fill, KNN)
- Duplicate detection and removal
- Outlier detection and handling (IQR, Z-score)
- Data type casting and normalization
- String trimming and standardization

**Methods:**
```python
class DataCleaner:
    def __init__(self, numeric_strategy='median', categorical_strategy='most_frequent')
    def remove_duplicates(self, df, subset=None) -> pd.DataFrame
    def handle_missing_values(self, df) -> pd.DataFrame
    def handle_outliers(self, df, method='iqr', threshold=1.5) -> pd.DataFrame
    def cast_data_types(self, df) -> pd.DataFrame
    def get_cleaning_report(self) -> Dict[str, Any]
```

**Imputation Strategies:**
- **Numeric:** mean, median, mode, forward-fill, backward-fill, KNN
- **Categorical:** mode, constant, forward-fill, backward-fill
- **Binary:** mode, constant (0 or 1)

---

### 3. FeatureEncoder Class

**Purpose:** Encode categorical variables for ML models

**Key Features:**
- One-Hot Encoding (OHE) with sparse matrix support
- Label Encoding for ordinal variables
- Target Encoding for high-cardinality features
- Frequency Encoding
- Binary Encoding
- Handle unknown categories during inference
- Save/load encoder artifacts

**Methods:**
```python
class FeatureEncoder:
    def __init__(self, encoding_strategy='onehot', handle_unknown='ignore')
    def fit(self, df, columns=None) -> 'FeatureEncoder'
    def transform(self, df) -> pd.DataFrame
    def fit_transform(self, df, columns=None) -> pd.DataFrame
    def inverse_transform(self, df) -> pd.DataFrame
    def save(self, path) -> None
    def load(self, path) -> 'FeatureEncoder'
    def get_feature_names(self) -> List[str]
```

**Encoding Strategies:**
- **OneHot:** Best for low-cardinality categorical features
- **Label:** Best for ordinal features with natural ordering
- **Target:** Best for high-cardinality features (uses target correlation)
- **Frequency:** Encodes by category frequency
- **Binary:** Converts categories to binary representation

---

### 4. FeatureScaler Class

**Purpose:** Scale numerical features for ML models

**Key Features:**
- StandardScaler (z-score normalization)
- MinMaxScaler (0-1 normalization)
- RobustScaler (median and IQR-based, robust to outliers)
- MaxAbsScaler (scales by maximum absolute value)
- Save/load scaler artifacts
- Selective column scaling

**Methods:**
```python
class FeatureScaler:
    def __init__(self, scaling_strategy='standard', columns=None)
    def fit(self, df) -> 'FeatureScaler'
    def transform(self, df) -> pd.DataFrame
    def fit_transform(self, df) -> pd.DataFrame
    def inverse_transform(self, df) -> pd.DataFrame
    def save(self, path) -> None
    def load(self, path) -> 'FeatureScaler'
```

**Scaling Strategies:**
- **Standard:** Mean=0, Std=1 (assumes normal distribution)
- **MinMax:** Scales to [0, 1] range
- **Robust:** Uses median and IQR (robust to outliers)
- **MaxAbs:** Scales by maximum absolute value (preserves sparsity)

---

### 5. FeatureEngineer Class

**Purpose:** Create derived features and transformations

**Key Features:**
- RFM score calculation (Recency, Frequency, Monetary)
- Binning/bucketing (equal-width, equal-frequency, custom)
- Polynomial features
- Interaction terms
- Log/sqrt transformations
- Date/time feature extraction
- Custom feature functions

**Methods:**
```python
class FeatureEngineer:
    def __init__(self)
    def add_rfm_features(self, df) -> pd.DataFrame
    def add_binned_features(self, df, column, bins, labels=None) -> pd.DataFrame
    def add_polynomial_features(self, df, columns, degree=2) -> pd.DataFrame
    def add_interaction_features(self, df, column_pairs) -> pd.DataFrame
    def add_log_features(self, df, columns) -> pd.DataFrame
    def add_datetime_features(self, df, column) -> pd.DataFrame
    def add_custom_feature(self, df, func, name) -> pd.DataFrame
```

**Feature Types:**
- **RFM Features:** Recency, Frequency, Monetary scores and segments
- **Binned Features:** Tenure buckets, age groups, value tiers
- **Polynomial:** x², x³, etc. for capturing non-linear relationships
- **Interactions:** x₁ × x₂ for capturing feature interactions
- **Transformations:** log(x), √x for handling skewed distributions

---

### 6. DataPreprocessor Class (Orchestrator)

**Purpose:** Coordinate all preprocessing components in a unified pipeline

**Key Features:**
- Sequential pipeline execution
- Component configuration
- Train/test split with stratification
- Pipeline persistence (save/load entire pipeline)
- Preprocessing report generation
- Support for both training and inference modes

**Methods:**
```python
class DataPreprocessor:
    def __init__(self, config=None)
    def add_step(self, name, component, **kwargs) -> 'DataPreprocessor'
    def fit(self, df, target_col=None) -> 'DataPreprocessor'
    def transform(self, df) -> pd.DataFrame
    def fit_transform(self, df, target_col=None) -> pd.DataFrame
    def split_data(self, df, test_size=0.2, stratify=True) -> Tuple
    def save_pipeline(self, path) -> None
    def load_pipeline(self, path) -> 'DataPreprocessor'
    def get_preprocessing_report(self) -> Dict[str, Any]
```

**Pipeline Configuration:**
```python
config = {
    'loader': {'expected_columns': FEATURE_COLS + [TARGET_COL]},
    'cleaner': {
        'numeric_strategy': 'median',
        'categorical_strategy': 'most_frequent',
        'remove_duplicates': True
    },
    'encoder': {
        'strategy': 'onehot',
        'columns': CATEGORICAL_COLS,
        'handle_unknown': 'ignore'
    },
    'scaler': {
        'strategy': 'standard',
        'columns': NUMERIC_COLS
    },
    'engineer': {
        'add_rfm': True,
        'add_bins': True
    }
}
```

---

## Implementation Plan

### Phase 1: Core Classes (Priority: High)
1. ✅ **DataLoader** - CSV loading and validation
2. ✅ **DataCleaner** - Missing values, duplicates, types
3. ✅ **FeatureEncoder** - Categorical encoding
4. ✅ **FeatureScaler** - Numerical scaling

### Phase 2: Advanced Features (Priority: Medium)
5. ✅ **FeatureEngineer** - Derived features and transformations
6. ✅ **DataPreprocessor** - Pipeline orchestration
7. ✅ **Model Persistence** - Save/load encoders and scalers
8. ✅ **Train/Test Split** - Stratified splitting

### Phase 3: Quality & Documentation (Priority: Medium)
9. ✅ **Data Validation** - Quality checks and reporting
10. ✅ **Error Handling** - Comprehensive exception handling
11. ✅ **Logging** - Detailed operation logging
12. ✅ **Documentation** - Docstrings and usage examples

### Phase 4: Backward Compatibility (Priority: High)
13. ✅ **Wrapper Functions** - Maintain existing function signatures
14. ✅ **Integration Testing** - Ensure existing code still works
15. ✅ **Migration Guide** - Document transition path

---

## Backward Compatibility Strategy

### Existing Functions to Maintain

```python
# Keep these functions as wrappers around new classes
def load_csv(path) -> pd.DataFrame
def basic_clean(df) -> pd.DataFrame
def handle_missing(df) -> pd.DataFrame
def add_derived_features(df) -> pd.DataFrame
def prepare_data_for_analysis(df) -> pd.DataFrame
```

### Implementation Approach

```python
# Example: Maintain load_csv as a wrapper
def load_csv(path):
    """Legacy function - wraps DataLoader class"""
    loader = DataLoader()
    return loader.load_csv(path)

# Example: Maintain basic_clean as a wrapper
def basic_clean(df):
    """Legacy function - wraps DataCleaner class"""
    cleaner = DataCleaner()
    df = cleaner.remove_duplicates(df)
    df = cleaner.cast_data_types(df)
    return df
```

---

## Usage Examples

### Example 1: Simple Analytics Workflow (Existing Pattern)

```python
from src.data_prep import load_csv, prepare_data_for_analysis

# Load and prepare data (backward compatible)
df = load_csv('data/sample_churn.csv')
df_clean = prepare_data_for_analysis(df)
```

### Example 2: ML Training Workflow (New Pattern)

```python
from src.data_prep import DataPreprocessor
from src.helpers import NUMERIC_COLS, CATEGORICAL_COLS, TARGET_COL

# Create preprocessing pipeline
preprocessor = DataPreprocessor()

# Add preprocessing steps
preprocessor.add_step('cleaner', DataCleaner(
    numeric_strategy='median',
    categorical_strategy='most_frequent'
))
preprocessor.add_step('encoder', FeatureEncoder(
    encoding_strategy='onehot',
    columns=CATEGORICAL_COLS
))
preprocessor.add_step('scaler', FeatureScaler(
    scaling_strategy='standard',
    columns=NUMERIC_COLS
))

# Load data
df = load_csv('data/sample_churn.csv')

# Fit and transform training data
df_processed = preprocessor.fit_transform(df, target_col=TARGET_COL)

# Split into train/test
X_train, X_test, y_train, y_test = preprocessor.split_data(
    df_processed, 
    test_size=0.2, 
    stratify=True
)

# Save pipeline for inference
preprocessor.save_pipeline('models/preprocessing_pipeline.pkl')
```

### Example 3: ML Inference Workflow

```python
from src.data_prep import DataPreprocessor

# Load saved pipeline
preprocessor = DataPreprocessor()
preprocessor.load_pipeline('models/preprocessing_pipeline.pkl')

# Load new data
df_new = load_csv('data/new_customers.csv')

# Transform using fitted pipeline (no fitting!)
df_processed = preprocessor.transform(df_new)

# Ready for model prediction
predictions = model.predict(df_processed)
```

### Example 4: Custom Pipeline Configuration

```python
from src.data_prep import DataPreprocessor

# Define custom configuration
config = {
    'cleaner': {
        'numeric_strategy': 'knn',  # Use KNN imputation
        'categorical_strategy': 'constant',
        'constant_value': 'Unknown',
        'outlier_method': 'iqr',
        'outlier_threshold': 1.5
    },
    'encoder': {
        'strategy': 'target',  # Use target encoding
        'columns': ['region', 'payment_type'],
        'smoothing': 1.0
    },
    'scaler': {
        'strategy': 'robust',  # Use robust scaler
        'columns': NUMERIC_COLS
    },
    'engineer': {
        'add_rfm': True,
        'add_polynomial': True,
        'polynomial_degree': 2,
        'polynomial_columns': ['age', 'tenure_months']
    }
}

# Create pipeline with configuration
preprocessor = DataPreprocessor(config=config)
df_processed = preprocessor.fit_transform(df, target_col=TARGET_COL)
```

---

## Data Quality Reporting

### Preprocessing Report Structure

```python
{
    'data_summary': {
        'total_rows': 2000,
        'total_columns': 13,
        'memory_usage': '156.3 KB'
    },
    'cleaning_report': {
        'duplicates_removed': 5,
        'missing_values_before': 47,
        'missing_values_after': 0,
        'outliers_detected': 12,
        'outliers_handled': 12
    },
    'encoding_report': {
        'columns_encoded': ['gender', 'region', 'payment_type'],
        'encoding_strategy': 'onehot',
        'new_features_created': 8,
        'categories_per_column': {
            'gender': 3,
            'region': 3,
            'payment_type': 4
        }
    },
    'scaling_report': {
        'columns_scaled': NUMERIC_COLS,
        'scaling_strategy': 'standard',
        'scaling_params': {
            'age': {'mean': 32.5, 'std': 12.3},
            'total_orders': {'mean': 5.2, 'std': 3.1}
        }
    },
    'feature_engineering_report': {
        'rfm_features_added': True,
        'binned_features_added': ['tenure_bucket', 'recency_bucket'],
        'polynomial_features_added': 3,
        'total_features_before': 13,
        'total_features_after': 28
    }
}
```

---

## File Structure

```
src/
├── data_prep.py (refactored with classes + backward compatible functions)
├── helpers.py (existing - no changes)
├── eda_utils.py (existing - no changes)
├── biz_metrics.py (existing - no changes)
└── sql_utils.py (existing - no changes)

models/
├── encoders_scalers/
│   ├── ohe_encoder.pkl (categorical encoder)
│   ├── num_scaler.pkl (numerical scaler)
│   └── preprocessing_pipeline.pkl (full pipeline)

tests/
├── smoke_tests.py (update to test new classes)
└── test_data_prep.py (new - comprehensive unit tests)

docs/
└── data_prep_usage_guide.md (new - usage examples)
```

---

## Testing Strategy

### Unit Tests
- Test each class independently
- Test edge cases (empty data, all missing, single row)
- Test error handling
- Test save/load functionality

### Integration Tests
- Test full pipeline execution
- Test backward compatibility
- Test with actual sample data
- Test train/inference workflow

### Performance Tests
- Test with large datasets (>100k rows)
- Memory usage profiling
- Execution time benchmarking

---

## Migration Path

### For Existing Code (No Changes Required)
```python
# This code continues to work without modification
from src.data_prep import load_csv, prepare_data_for_analysis

df = load_csv('data/sample_churn.csv')
df_clean = prepare_data_for_analysis(df)
```

### For New ML Workflows
```python
# Use new class-based approach
from src.data_prep import DataPreprocessor

preprocessor = DataPreprocessor()
# ... configure and use pipeline
```

### Gradual Migration
1. **Phase 1:** Keep using existing functions (no changes)
2. **Phase 2:** Start using new classes for new features
3. **Phase 3:** Gradually migrate existing code to new classes
4. **Phase 4:** Deprecate old functions (with warnings)

---

## Success Metrics

### Functional Requirements
- ✅ All existing functionality preserved
- ✅ Categorical encoding implemented
- ✅ Numerical scaling implemented
- ✅ Train/test split implemented
- ✅ Model persistence implemented
- ✅ Data quality reporting implemented

### Non-Functional Requirements
- ✅ Backward compatibility maintained
- ✅ Code coverage >80%
- ✅ Documentation complete
- ✅ Performance acceptable (<2x slower than current)
- ✅ Memory usage acceptable (<1.5x current)

---

## Next Steps

1. **Review and Approve Design** - Get stakeholder feedback
2. **Create Implementation Branch** - Set up development environment
3. **Implement Core Classes** - Start with DataLoader, DataCleaner
4. **Add ML Features** - Implement FeatureEncoder, FeatureScaler
5. **Build Orchestrator** - Create DataPreprocessor pipeline
6. **Write Tests** - Comprehensive unit and integration tests
7. **Update Documentation** - Usage guides and API docs
8. **Code Review** - Peer review and feedback
9. **Merge to Main** - Deploy to production

---

## Questions for Stakeholders

1. **Priority:** Should we prioritize backward compatibility or new features?
2. **Configuration:** Do we need YAML/JSON config file support?
3. **Performance:** What are acceptable performance benchmarks?
4. **Testing:** What level of test coverage is required?
5. **Documentation:** What documentation format is preferred?
6. **Deployment:** When should this be deployed to production?

---

## Conclusion

This refactoring will transform the data preparation module into a robust, extensible, and ML-ready system while maintaining full backward compatibility. The class-based architecture provides clear separation of concerns, making the code easier to maintain, test, and extend.

The modular design allows users to:
- Use existing functions for simple analytics workflows
- Build custom ML pipelines with fine-grained control
- Save and reuse preprocessing pipelines
- Generate comprehensive data quality reports
- Handle both training and inference scenarios

**Estimated Implementation Time:** 3-4 weeks
**Risk Level:** Low (backward compatibility maintained)
**Impact:** High (enables ML workflows, improves code quality)