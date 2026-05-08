"""
Run monitoring/monitor.py as a SageMaker Processing Job.
"""
import sagemaker
from sagemaker.processing import ScriptProcessor
import boto3
import os

role = os.environ.get("SAGEMAKER_ROLE", "SageMakerRole")  # Replace with your SageMaker execution role ARN
region = boto3.Session().region_name
sess = sagemaker.Session()

# Use the same image as your training job, or a standard Python image
script_processor = ScriptProcessor(
    image_uri=f"683313688378.dkr.ecr.{region}.amazonaws.com/sagemaker-scikit-learn:0.23-1-cpu-py3",
    command=["python3"],
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    base_job_name="monitoring-job",
    sagemaker_session=sess,
)

script_processor.run(
    code="../monitoring/monitor.py",
    inputs=[],
    outputs=[],
    wait=True,
)
