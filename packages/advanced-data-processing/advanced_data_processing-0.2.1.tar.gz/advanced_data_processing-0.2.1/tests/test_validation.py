import pytest
import pandas as pd
import numpy as np
from adv_data_processing.data_validation import validate_data_schema

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'col1': [1.0, 2.0, 3.0, 4.0, 5.0],
        'col2': ['A', 'B', 'C', 'D', 'E'],
        'col3': [1.1, 2.2, 3.3, 4.4, 5.5]
    })

def test_validate_data_schema_basic(sample_df):
    schema = {
        'col1': {
            'type': 'float64',
            'range': [0, 10]
        }
    }
    results = validate_data_schema(sample_df, schema)
    assert results['valid'], f"Validation failed with results: {results}"
    assert len(results['violations']) == 0
    assert len(results['type_mismatches']) == 0
    assert len(results['range_violations']) == 0

def test_validate_data_schema_range_violation(sample_df):
    schema = {
        'col1': {
            'type': 'float64',
            'range': [0, 3]
        }
    }
    results = validate_data_schema(sample_df, schema)
    assert not results['valid']
    assert len(results['range_violations']) > 0
    assert all(v['value'] > 3 for v in results['range_violations'])

def test_validate_data_schema_type_mismatch(sample_df):
    schema = {
        'col1': {
            'type': 'int32',
            'range': [0, 10]
        }
    }
    results = validate_data_schema(sample_df, schema)
    assert not results['valid']
    assert len(results['type_mismatches']) == 1
    assert results['type_mismatches'][0]['expected'] == 'int32'
    assert results['type_mismatches'][0]['actual'] == 'float64'

def test_validate_data_schema_missing_column(sample_df):
    schema = {
        'missing_column': {
            'type': 'float64',
            'range': [0, 10]
        }
    }
    results = validate_data_schema(sample_df, schema)
    assert results['valid']  # Missing columns should not cause validation failure
    assert len(results['violations']) == 0 