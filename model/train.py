# train.py
"""
SageMaker-compatible training script for demand forecasting using Prophet and Feast.
Fetches features from Feast (DynamoDB online store), trains Prophet, and saves model artifact.
"""
import os
import pandas as pd
from prophet import Prophet
import pickle
from feast import FeatureStore

# SageMaker passes input data location as an environment variable
input_data_dir = os.environ.get('SM_CHANNEL_TRAIN', '/opt/ml/input/data/train')
output_model_dir = os.environ.get('SM_MODEL_DIR', '/opt/ml/model')

# Load entity dataframe (e.g., store_id, item_id, date)
entity_df = pd.read_csv(os.path.join(input_data_dir, 'entities.csv'))

# Connect to Feast feature store (assumes feature_store.yaml is in the container or working dir)
store = FeatureStore(repo_path="/opt/ml/code/feature_store")  # Adjust path as needed

# Fetch features for training
features = [
    "sales_features:price",
    "sales_features:promotion",
    "sales_features:seasonality",
]
feature_df = store.get_online_features(features=features, entity_rows=entity_df.to_dict(orient="records")).to_df()

# Merge features with entity_df for Prophet
df = pd.concat([entity_df, feature_df], axis=1)
df.rename(columns={'date': 'ds', 'sales': 'y'}, inplace=True)

# Train Prophet model
model = Prophet()
model.fit(df)

# Save model artifact for SageMaker
with open(os.path.join(output_model_dir, 'prophet_model.pkl'), 'wb') as f:
    pickle.dump(model, f)
