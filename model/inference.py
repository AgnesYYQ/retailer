# inference.py
"""
Runs batch or real-time inference using the trained model.
"""
import pandas as pd
from prophet import Prophet
import pickle

# Load model
with open('prophet_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load data for prediction
df = pd.read_csv('predict.csv')  # Replace with your data path
forecast = model.predict(df)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
