
import pandas as pd
import pickle
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.offline as py
import numpy as np
import os

# --- Mock Feast Feature Store ---
class MockFeastStore:
    def get_online_features(self, features, entity_rows):
        # Return a DataFrame with random/mock features
        df = pd.DataFrame(entity_rows)
        for f in features:
            fname = f.split(":")[1]
            df[fname] = np.random.rand(len(df))
        return df

# --- Mock Kafka Consumer ---
class MockKafkaConsumer:
    def __init__(self, topic, bootstrap_servers, **kwargs):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
    def __iter__(self):
        # Simulate 5 events
        for i in range(5):
            yield {'value': {'store_id': i, 'item_id': i, 'date': f'2024-01-0{i+1}', 'sales': np.random.randint(10, 100)}}

print("===== Mock Kafka Event Ingestion Test =====")
consumer = MockKafkaConsumer('sales_events', ['localhost:9092'])
events = [msg['value'] for msg in consumer]
entity_df = pd.DataFrame(events)
print(entity_df)
print()

print("===== Mock Feast Feature Fetch Test =====")
mock_store = MockFeastStore()
features = ["sales_features:price", "sales_features:promotion", "sales_features:seasonality"]
feature_df = mock_store.get_online_features(features, entity_df.to_dict(orient="records"))
print(feature_df)
print()

print("===== Load Trained Model Test =====")
with open('prophet_model.pkl', 'rb') as f:
    model = pickle.load(f)
print("Model loaded successfully.\n")

print("===== Prediction Test (with Features, Historical) =====")
# This predicts on the same (historical) data, mainly for validation
if 'ds' not in feature_df:
    feature_df['ds'] = entity_df['date']
    feature_df['y'] = entity_df['sales']
forecast_hist = model.predict(feature_df)
print('Historical Prediction:')
print(forecast_hist[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
print()

print("===== Forecast Test (Future Dates) =====")
# Generate future dates for forecasting
future_dates = pd.date_range(start=entity_df['date'].max(), periods=8, freq='D')[1:]
future_entity_df = pd.DataFrame({
    'store_id': [0]*len(future_dates),
    'item_id': [0]*len(future_dates),
    'date': future_dates.strftime('%Y-%m-%d'),
    'sales': [np.nan]*len(future_dates)  # Unknown future sales
})
future_feature_df = mock_store.get_online_features(features, future_entity_df.to_dict(orient="records"))
future_feature_df['ds'] = future_entity_df['date']
# Prophet expects 'y' column, but for forecasting it can be NaN
future_feature_df['y'] = np.nan
forecast_future = model.predict(future_feature_df)
print('Forecast for Future Dates:')
print(forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
print()
# Note: The forecast uses the trained Prophet model, which was fit on historical data above.

print("===== Evaluation (MAPE) Test =====")
def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
actuals = pd.read_csv('actuals.csv')
# Use forecast_hist (historical prediction) for MAPE evaluation
print('MAPE:', mape(actuals['sales'], forecast_hist['yhat'][-len(actuals):]))
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
# Plot historical prediction
fig1 = plot_plotly(model, forecast_hist)
py.plot(fig1, filename='forecast_hist.html', auto_open=False)
# Plot future forecast
fig2 = plot_plotly(model, forecast_future)
py.plot(fig2, filename='forecast_future.html', auto_open=False)
# Plot components for historical prediction
fig3 = plot_components_plotly(model, forecast_hist)
py.plot(fig3, filename='components_hist.html', auto_open=False)
# Plot components for future forecast
fig4 = plot_components_plotly(model, forecast_future)
py.plot(fig4, filename='components_future.html', auto_open=False)
print('Saved forecast_hist.html, forecast_future.html, components_hist.html, and components_future.html for visualization.\n')

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