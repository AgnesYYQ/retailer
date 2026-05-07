# alerting.py
"""
Sends alerts on drift or performance issues.
"""
def send_alert(message):
    # Replace with integration to email, Slack, etc.
    print(f'ALERT: {message}')

# Example usage
send_alert('Drift detected in demand forecast!')
