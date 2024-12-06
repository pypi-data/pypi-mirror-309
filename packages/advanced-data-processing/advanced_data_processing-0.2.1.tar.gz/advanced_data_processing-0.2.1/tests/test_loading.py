import pytest
from adv_data_processing.loading import load_data, load_from_csv
import pandas as pd
import dask.dataframe as dd
import tempfile
import os

def test_load_from_csv():
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w', delete=False) as f:
        pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['x', 'y', 'z']
        }).to_csv(f.name, index=False)
        
        # Test loading
        df = load_from_csv(f.name)
        assert isinstance(df, dd.DataFrame)
        assert list(df.columns) == ['A', 'B']
        assert df.npartitions > 0
        
    os.unlink(f.name)

def test_load_data_unsupported_format():
    with pytest.raises(ValueError):
        load_data('file.unsupported')

@pytest.mark.parametrize("file_type,content", [
    ('.csv', 'a,b\n1,2\n3,4'),
    ('.json', '{"a": [1,3], "b": [2,4]}'),
])
def test_load_data_formats(file_type, content):
    with tempfile.NamedTemporaryFile(suffix=file_type, mode='w', delete=False) as f:
        f.write(content)
        f.flush()
        
        df = load_data(f.name)
        assert isinstance(df, dd.DataFrame)
        assert df.npartitions > 0
        
    os.unlink(f.name) 