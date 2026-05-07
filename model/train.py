# train.py
"""
Trains Prophet or Transformer-based models on historical data.
"""
import pandas as pd
from prophet import Prophet
import pickle

# Load your training data
df = pd.read_csv('train.csv')  # Replace with your data path
df.rename(columns={'date': 'ds', 'sales': 'y'}, inplace=True)

model = Prophet()
model.fit(df)

with open('prophet_model.pkl', 'wb') as f:
    pickle.dump(model, f)
