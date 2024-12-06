import pytest
import pandas as pd
import dask.dataframe as dd
from adv_data_processing.feature_engineering import (
    auto_feature_engineering,
    create_polynomial_features,
    create_interaction_features
)

def test_auto_feature_engineering(sample_dask_df):
    config = {
        'create_polynomial_features': True,
        'polynomial_degree': 2,
        'create_interaction_features': True
    }
    
    result = auto_feature_engineering(sample_dask_df, 'target', config)
    assert isinstance(result, dd.DataFrame)
    assert len(result.columns) > len(sample_dask_df.columns)

def test_create_polynomial_features(sample_dask_df):
    result = create_polynomial_features(sample_dask_df, degree=2)
    numeric_cols = sample_dask_df.select_dtypes(include=['int64', 'float64']).columns
    expected_features = len(numeric_cols) * (len(numeric_cols) + 1) // 2
    
    poly_cols = [col for col in result.columns if col.startswith('poly_')]
    assert len(poly_cols) == expected_features

def test_invalid_input():
    with pytest.raises(TypeError):
        auto_feature_engineering(pd.DataFrame(), 'target', {})

def test_missing_target():
    df = dd.from_pandas(pd.DataFrame({'A': [1, 2, 3]}), npartitions=1)
    with pytest.raises(ValueError):
        auto_feature_engineering(df, 'missing_target', {}) 