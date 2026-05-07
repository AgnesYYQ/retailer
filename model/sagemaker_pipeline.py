# sagemaker_pipeline.py
"""
SageMaker training pipeline for demand forecasting using Prophet and Feast.
Expects entities.csv in the input S3 location and feature_store/ in the container/code.
"""
import sagemaker
from sagemaker.sklearn.estimator import SKLearn

role = 'SageMakerRole'  # Replace with your IAM role
estimator = SKLearn(
    entry_point='train.py',
    role=role,
    instance_type='ml.m5.large',
    framework_version='0.23-1',
    source_dir='.',  # Ensure feature_store/ is included
    dependencies=['../feature_store'],
)
estimator.fit({'train': 's3://your-bucket/entities.csv'})
