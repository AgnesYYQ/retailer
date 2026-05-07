# batch_loader.py
"""
Loads historical sales data from S3 for batch processing.
Replace placeholders with your S3 bucket and credentials.
"""
import boto3
import pandas as pd

S3_BUCKET = 'your-bucket'  # Replace
S3_KEY = 'historical/sales.csv'  # Replace

s3 = boto3.client('s3')
obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
df = pd.read_csv(obj['Body'])
print(df.head())
