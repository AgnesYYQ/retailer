# monitor.py
"""
Tracks forecast accuracy (MAPE), detects drift, triggers retraining.
"""
import pandas as pd

def mape(y_true, y_pred):
    return (abs((y_true - y_pred) / y_true)).mean() * 100

# Example usage
y_true = pd.Series([100, 200, 300])
y_pred = pd.Series([110, 190, 310])
print('MAPE:', mape(y_true, y_pred))

# TODO: Add drift detection and retraining trigger
