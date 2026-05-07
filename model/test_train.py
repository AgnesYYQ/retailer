import pandas as pd
import pickle
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.offline as py
import numpy as np
import os

print("===== Load Trained Model Test =====")
with open('prophet_model.pkl', 'rb') as f:
    model = pickle.load(f)
print("Model loaded successfully.\n")

print("===== Prediction Test =====")
future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)
print('Forecast:')
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7))
print()

print("===== Evaluation (MAPE) Test =====")
def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
print("(To use, uncomment and provide actuals for the forecast period)")
# actuals = pd.read_csv('actuals.csv')
# print('MAPE:', mape(actuals['sales'], forecast['yhat'][-len(actuals):]))
print()

print("===== Add Features (Holiday) Test =====")
holidays = pd.DataFrame({
    'holiday': 'promo',
    'ds': pd.to_datetime(['2024-01-05', '2024-01-12']),
    'lower_window': 0,
    'upper_window': 1,
})
model_with_holiday = Prophet(holidays=holidays)
model_with_holiday.fit(pd.read_csv('train.csv').rename(columns={'date': 'ds', 'sales': 'y'}))
print("Holiday feature added and model retrained.\n")

print("===== Visualization Test =====")
fig1 = plot_plotly(model, forecast)
py.plot(fig1, filename='forecast.html', auto_open=False)
fig2 = plot_components_plotly(model, forecast)
py.plot(fig2, filename='components.html', auto_open=False)
print('Saved forecast.html and components.html for visualization.\n')

print("===== Automation (Retraining) Test =====")
if os.path.exists('new_train.csv'):
    print('New data found, retraining...')
    df_new = pd.read_csv('new_train.csv').rename(columns={'date': 'ds', 'sales': 'y'})
    model_new = Prophet()
    model_new.fit(df_new)
    with open('prophet_model_new.pkl', 'wb') as f:
        pickle.dump(model_new, f)
    print('Retrained and saved as prophet_model_new.pkl')
else:
    print('No new data for retraining.')