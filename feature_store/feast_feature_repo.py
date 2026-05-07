# feast_feature_repo.py
"""
Defines Feast feature sets (price, promotion, seasonality, etc).
Replace with your actual feature definitions.
"""
from feast import FeatureStore, Entity, FeatureView, Field
from feast.types import Float32, Int64

# Example entity
demand = Entity(name="demand", join_keys=["store_id", "item_id"])

# Example feature view
sales_fv = FeatureView(
    name="sales_features",
    entities=[demand],
    schema=[
        Field(name="price", dtype=Float32),
        Field(name="promotion", dtype=Int64),
        Field(name="seasonality", dtype=Float32),
    ],
    online=True,
    batch_source=None,  # Replace with your batch source
)
