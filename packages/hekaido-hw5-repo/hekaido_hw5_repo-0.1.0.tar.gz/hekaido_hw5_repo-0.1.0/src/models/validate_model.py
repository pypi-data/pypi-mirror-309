"""
Provides function for model validation
"""

from sklearn.metrics import accuracy_score

def validate(model, x, y):
    """
    Returns metric of trained model on validation dataset
    
    Parameters:
        model: trained model
        x: validation data
        y: validation targets
    """
    predict = model.predict(x)
    return accuracy_score(y, predict)
