"""
Generates a SageMaker solution architecture diagram using diagrams (https://diagrams.mingrammer.com/).
Run this script to produce a PNG for your README.
"""
from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda, EC2, ECS
from diagrams.aws.ml import Sagemaker, SagemakerModel
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.onprem.monitoring import Prometheus

with Diagram("SageMaker Solution Architecture", show=False, filename="sagemaker_architecture", direction="LR"):
    with Cluster("Ingestion"):
        kafka = ManagedStreamingForKafka("Kafka (MSK)")
        batch = S3("Batch Data (S3)")
    with Cluster("Feature Store"):
        feast = Dynamodb("Feast (DynamoDB)")
    with Cluster("Training"):
        training = Sagemaker("SageMaker Training Job")
    with Cluster("Model Registry"):
        model = SagemakerModel("Model Artifact")
    with Cluster("Serving"):
        endpoint = Sagemaker("SageMaker Endpoint")
    with Cluster("Monitoring"):
        monitoring = Prometheus("Monitoring & Retraining")

    kafka >> feast
    batch >> feast
    feast >> training
    training >> model
    model >> endpoint
    endpoint >> monitoring
    monitoring >> training
    endpoint >> feast
    training >> feast
