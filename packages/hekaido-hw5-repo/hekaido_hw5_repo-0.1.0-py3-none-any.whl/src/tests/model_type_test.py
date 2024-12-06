"""
    Testing function for edge case
"""
import pytest

from src.data.make_dataset import make_dataset
from src.config.data_config import DataConfig
from src.config.model_config import ModelConfig
from src.models.train_model import train_model

def test_train_model():
    data_config  = DataConfig()
    model_config = ModelConfig(model_type='test')
    x_train, _, y_train, _ = make_dataset(data_config)
    model = train_model(model_config, x_train, y_train)
    assert model is None
