"""
Provides function for model training
"""

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

def train_model(model_config, x, y):
    """
    Returns trained model on data
    
    Parameters:
        model_config: config for model initialization
        X: train data
        y: train targets
    Return:
        model: model trained on data
    """
    if model_config.model_type == 'logistic_regression':
        model = LogisticRegression()
    elif model_config.model_type == 'random_forest':
        model = RandomForestClassifier(
            n_estimators=model_config.n_estimators,
            max_depth=model_config.max_depth
        )
    elif model_config.model_type == 'decision_tree':
        model = DecisionTreeClassifier(max_depth=model_config.max_depth)
    else:
        return None
    model.fit(x, y)
    return model
