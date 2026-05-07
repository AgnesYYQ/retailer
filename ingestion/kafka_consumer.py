# kafka_consumer.py
"""
Consumes real-time sales events from Kafka and writes to feature store or S3.
Replace placeholders with your Kafka broker and topic details.
"""
from kafka import KafkaConsumer
import json

KAFKA_BROKER = 'localhost:9092'  # Replace with your broker
KAFKA_TOPIC = 'sales_events'     # Replace with your topic

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

for message in consumer:
    event = message.value
    # TODO: Write event to feature store or S3
    print(event)
