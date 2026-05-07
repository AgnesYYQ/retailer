# app.py
"""
FastAPI app for model inference API.
"""
from fastapi import FastAPI
import pickle
import pandas as pd

app = FastAPI()

with open('prophet_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.post('/predict')
def predict(data: dict):
    df = pd.DataFrame([data])
    forecast = model.predict(df)
    return forecast[['ds', 'yhat']].to_dict(orient='records')
