# monitor.py
"""
Tracks forecast accuracy (MAPE), detects drift, triggers retraining.
"""
import pandas as pd

def mape(y_true, y_pred):
    return (abs((y_true - y_pred) / y_true)).mean() * 100

# Example usage
y_true = pd.Series([100, 200, 300])
y_pred = pd.Series([110, 190, 310])
print('MAPE:', mape(y_true, y_pred))


# --- Drift Detection and Retraining Trigger ---

import numpy as np
import boto3
import os

def send_sns_alert(message, subject="Model Monitoring Alert"):
    sns_topic_arn = os.environ.get("SNS_TOPIC_ARN")  # Set this env var to your SNS topic ARN
    if not sns_topic_arn:
        print("SNS_TOPIC_ARN not set, skipping SNS alert.")
        return
    sns = boto3.client("sns")
    sns.publish(TopicArn=sns_topic_arn, Message=message, Subject=subject)

def detect_drift(y_true, y_pred, window=3, drift_threshold=0.2):
    # Simple drift: if mean absolute error in last window increases by >drift_threshold over previous window
    errors = abs(y_true - y_pred)
    if len(errors) < 2 * window:
        return False
    prev = errors[-2*window:-window].mean()
    curr = errors[-window:].mean()
    drift = (curr - prev) / (prev + 1e-8)
    return drift > drift_threshold

def monitor_and_alert(y_true, y_pred, mape_threshold=10, drift_window=3, drift_threshold=0.2):
    mape_val = mape(y_true, y_pred)
    print(f"MAPE: {mape_val:.2f}%")
    alert_msgs = []
    if mape_val > mape_threshold:
        msg = f"ALERT: MAPE {mape_val:.2f}% exceeds threshold {mape_threshold}%. Consider retraining."
        print(msg)
        alert_msgs.append(msg)
    if detect_drift(y_true, y_pred, window=drift_window, drift_threshold=drift_threshold):
        msg = f"ALERT: Drift detected in last {drift_window} points. Consider retraining."
        print(msg)
        alert_msgs.append(msg)
    if alert_msgs:
        send_sns_alert("\n".join(alert_msgs))

# Example usage with simulated data
y_true = pd.Series([100, 200, 300, 400, 500, 600])
y_pred = pd.Series([110, 190, 310, 420, 480, 700])
monitor_and_alert(y_true, y_pred)
