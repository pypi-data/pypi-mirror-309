"""
Provides config for model initialization
"""

from pydantic import BaseModel

class ModelConfig(BaseModel):
    """
    Class to configure dataset
    Parameters:
        model_type: type of the model used
        n_estimators: number of estimators (for decision tree)
        max_depth: max depth of desicion tree (for decision tree)
    """
    model_type: str
    n_estimators: int = 100
    max_depth: int = 10
