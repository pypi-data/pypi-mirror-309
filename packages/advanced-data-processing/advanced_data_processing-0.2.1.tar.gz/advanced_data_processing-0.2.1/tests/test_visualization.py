import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adv_data_processing.visualization import (
    plot_feature_importance,
    plot_correlation_matrix,
    plot_distribution,
    plot_wordcloud,
    PLOTTING_AVAILABLE,
    WORDCLOUD_AVAILABLE
)

@pytest.fixture(autouse=True)
def mpl_backend():
    """Configure matplotlib to use non-interactive backend."""
    plt.switch_backend('Agg')
    yield
    plt.close('all')

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [0.1, 0.2, 0.3, 0.4, 0.5],
        'target': [0, 1, 0, 1, 0]
    })

@pytest.mark.skipif(not PLOTTING_AVAILABLE, 
                    reason="Plotting dependencies not installed")
def test_plot_feature_importance(sample_df):
    feature_importance = {
        'feature1': 0.7,
        'feature2': 0.3
    }
    fig = plot_feature_importance(feature_importance)
    assert fig is not None
    plt.close(fig)

@pytest.mark.skipif(not PLOTTING_AVAILABLE, 
                    reason="Plotting dependencies not installed")
def test_plot_correlation_matrix(sample_df):
    fig = plot_correlation_matrix(sample_df)
    assert fig is not None
    plt.close(fig)

@pytest.mark.skipif(not PLOTTING_AVAILABLE, 
                    reason="Plotting dependencies not installed")
def test_plot_distribution(sample_df):
    fig = plot_distribution(sample_df['feature1'])
    assert fig is not None
    plt.close(fig)

@pytest.mark.skipif(not PLOTTING_AVAILABLE, 
                    reason="Plotting dependencies not installed")
def test_plot_distribution_with_target(sample_df):
    fig = plot_distribution(
        sample_df['feature1'],
        target=sample_df['target']
    )
    assert fig is not None
    plt.close(fig)

@pytest.mark.skipif(not WORDCLOUD_AVAILABLE,
                    reason="Wordcloud package not installed")
def test_plot_wordcloud():
    text = "test word cloud visualization text analytics data science"
    fig = plot_wordcloud(text)
    assert fig is not None
    plt.close(fig)

def test_plotting_without_dependencies(monkeypatch, sample_df):
    # Simulate missing plotting dependencies
    monkeypatch.setattr(
        'adv_data_processing.visualization.PLOTTING_AVAILABLE', 
        False
    )
    
    with pytest.raises(ImportError):
        plot_feature_importance({'feature1': 0.7})
        
    with pytest.raises(ImportError):
        plot_correlation_matrix(sample_df)
        
    with pytest.raises(ImportError):
        plot_distribution(sample_df['feature1'])

def test_wordcloud_without_dependencies(monkeypatch):
    # Simulate missing wordcloud dependency
    monkeypatch.setattr(
        'adv_data_processing.visualization.WORDCLOUD_AVAILABLE',
        False
    )
    
    with pytest.raises(ImportError):
        plot_wordcloud("test text")