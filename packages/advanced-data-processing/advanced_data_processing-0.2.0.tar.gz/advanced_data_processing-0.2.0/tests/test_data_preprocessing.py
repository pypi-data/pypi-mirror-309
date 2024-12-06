import pytest
import pandas as pd
import numpy as np
from adv_data_processing.data_preprocessing import (
    handle_missing_values,
    encode_categorical_variables,
    scale_numerical_features,
    preprocess_dataset
)

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'numeric1': [1.0, 2.0, np.nan, 4.0, 5.0],
        'numeric2': [10.0, np.nan, 30.0, 40.0, 50.0],
        'category1': ['A', 'B', 'A', None, 'C'],
        'category2': ['X', 'Y', 'Z', 'X', None]
    })

def test_handle_missing_values(sample_df):
    # Test with mean strategy
    df_mean = handle_missing_values(
        sample_df, 
        numeric_strategy='mean',
        categorical_strategy='most_frequent'
    )
    assert not df_mean.isnull().any().any()
    assert df_mean['numeric1'].iloc[2] == sample_df['numeric1'].mean()
    assert df_mean['numeric2'].iloc[1] == sample_df['numeric2'].mean()
    
    # Test with median strategy
    df_median = handle_missing_values(
        sample_df, 
        numeric_strategy='median',
        categorical_strategy='most_frequent'
    )
    assert not df_median.isnull().any().any()
    assert df_median['numeric1'].iloc[2] == sample_df['numeric1'].median()
    
    # Test with constant strategy
    df_constant = handle_missing_values(
        sample_df,
        numeric_strategy='constant',
        numeric_fill_value=0,
        categorical_strategy='constant',
        categorical_fill_value='MISSING'
    )
    assert not df_constant.isnull().any().any()
    assert df_constant['numeric1'].iloc[2] == 0
    assert df_constant['category1'].iloc[3] == 'MISSING'

def test_encode_categorical_variables(sample_df):
    # Test one-hot encoding
    df_onehot = encode_categorical_variables(
        sample_df.fillna('MISSING'),
        encoding_type='onehot'
    )
    assert 'category1_A' in df_onehot.columns
    assert 'category2_X' in df_onehot.columns
    assert 'category1' not in df_onehot.columns
    
    # Test label encoding
    df_label = encode_categorical_variables(
        sample_df.fillna('MISSING'),
        encoding_type='label'
    )
    assert df_label['category1'].dtype == 'int64'
    assert df_label['category2'].dtype == 'int64'
    
    # Test invalid encoding type
    with pytest.raises(ValueError):
        encode_categorical_variables(sample_df, encoding_type='invalid')

def test_scale_numerical_features(sample_df):
    # Only use numeric columns for filling
    numeric_cols = sample_df.select_dtypes(include=['int64', 'float64']).columns
    df_filled = sample_df.copy()
    df_filled[numeric_cols] = df_filled[numeric_cols].fillna(df_filled[numeric_cols].mean())
    
    # Test standardization
    df_standard = scale_numerical_features(
        df_filled,
        scaling_type='standard'
    )
    for col in numeric_cols:
        # Verify exact standardization
        assert abs(df_standard[col].mean()) < 1e-10  # Exactly 0
        assert abs(df_standard[col].std() - 1.0) < 1e-10  # Exactly 1
    
    # Test min-max scaling
    df_minmax = scale_numerical_features(
        df_filled,
        scaling_type='minmax'
    )
    for col in numeric_cols:
        assert df_minmax[col].min() == 0  # Exactly 0
        assert df_minmax[col].max() == 1  # Exactly 1
    
    # Test invalid scaling type
    with pytest.raises(ValueError):
        scale_numerical_features(df_filled, scaling_type='invalid')

def test_preprocess_dataset(sample_df):
    # Test full preprocessing pipeline
    df_processed = preprocess_dataset(
        sample_df,
        numeric_missing_strategy='mean',
        categorical_missing_strategy='most_frequent',
        encoding_type='onehot',
        scaling_type='standard'
    )
    
    # Check that there are no missing values
    assert not df_processed.isnull().any().any()
    
    # Check that categorical variables are encoded
    assert any(col.startswith('category1_') for col in df_processed.columns)
    
    # Check that numerical variables are scaled
    numeric_cols = df_processed.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        assert abs(df_processed[col].mean()) < 1e-10  # Exactly 0
        assert abs(df_processed[col].std() - 1.0) < 1e-10  # Exactly 1

def test_preprocess_dataset_with_custom_options(sample_df):
    # Test with different options
    df_processed = preprocess_dataset(
        sample_df,
        numeric_missing_strategy='constant',
        numeric_fill_value=0,
        categorical_missing_strategy='constant',
        categorical_fill_value='MISSING',
        encoding_type='label',
        scaling_type='minmax'
    )
    
    # Check that missing values are filled with constants
    assert (df_processed['numeric1'] == 0).any()
    assert df_processed['numeric1'].min() == pytest.approx(0, abs=1e-10)
    assert df_processed['numeric1'].max() == pytest.approx(1, abs=1e-10) 