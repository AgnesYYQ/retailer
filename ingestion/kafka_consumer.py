# kafka_consumer.py
"""
Consumes real-time sales events from Kafka and writes to feature store or S3.
Replace placeholders with your Kafka broker and topic details.
"""
import os
from kafka import KafkaConsumer
import json

# Example: Get MSK broker and topic from environment variables or SageMaker hyperparameters
KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'b-1.example.kafka.us-east-1.amazonaws.com:9092')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'sales_events')

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    security_protocol='PLAINTEXT',  # Use 'SSL' or 'SASL_SSL' if your MSK cluster is encrypted
    # Add SSL/SASL config here if needed
)

for message in consumer:
    event = message.value
    # TODO: Write event to feature store or S3
    print(event)
