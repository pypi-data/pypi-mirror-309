import pytest
import dask.dataframe as dd
from adv_data_processing.pipeline import process_data
from dask.distributed import Client

def test_process_data_basic(sample_config):
    with Client(n_workers=2):
        result = process_data(
            source=sample_config['source'],
            steps=['load', 'clean'],
            cleaning_strategies=sample_config['cleaning_strategies']
        )
        assert isinstance(result, dd.DataFrame)

def test_process_data_with_transformations(sample_config):
    with Client(n_workers=2):
        result = process_data(
            source=sample_config['source'],
            steps=['load', 'clean', 'transform'],
            cleaning_strategies=sample_config['cleaning_strategies'],
            numeric_features=sample_config['numeric_features'],
            categorical_features=sample_config['categorical_features']
        )
        assert isinstance(result, dd.DataFrame)

@pytest.mark.parametrize("invalid_step", [
    'invalid_step',
    123,
    None
])
def test_process_data_invalid_step(invalid_step, sample_config):
    with pytest.raises(ValueError):
        with Client(n_workers=2):
            process_data(
                source=sample_config['source'],
                steps=[invalid_step]
            ) 