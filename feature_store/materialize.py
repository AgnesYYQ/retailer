# materialize.py
"""
Materializes features for training and serving.
"""
from feast import FeatureStore

store = FeatureStore(repo_path=".")
store.materialize_incremental(end_date=None)  # Replace end_date as needed
