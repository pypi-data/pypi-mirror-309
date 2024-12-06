"""
Provides function for dataset generation
"""

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

def make_dataset(config):
    """
    Returns generated dataset depended on data generation config

    Parameters:
        config: data config on which dataset will be generated

    Returns:
        x_train: train data
        x_test: test data
        y_train: train targets
        y_test: test targets
    """
    x, y = make_classification(
        n_samples=config.n_samples,
        n_features=config.n_features,
        n_classes=config.n_classes,
        random_state=config.random_state
    )
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=config.test_size,
        random_state=config.random_state
    )
    return x_train, x_test, y_train, y_test
