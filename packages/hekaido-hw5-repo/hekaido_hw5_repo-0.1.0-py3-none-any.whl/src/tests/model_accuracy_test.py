"""
    Testing functions for accuracy
"""
import pytest

from src.data import make_dataset
from src.config import DataConfig
from src.config import ModelConfig
from src.models import train_model
from src.models import validate

@pytest.mark.parametrize("model_type",
    [
        ("logistic_regression"),
        ("random_forest"),
        ("decision_tree")
    ]
)
def test_train_model(model_type):
    data_config  = DataConfig()
    model_config = ModelConfig(model_type=model_type)
    x_train, x_test, y_train, y_test = make_dataset(data_config)
    model = train_model(model_config, x_train, y_train)
    accuracy = validate(model, x_test, y_test)
    assert accuracy > 0.5
