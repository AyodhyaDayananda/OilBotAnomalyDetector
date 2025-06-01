import requests

class SplunkLogger:
    def __init__(self, token, splunk_url):
        self.token = token
        self.splunk_url = splunk_url

    def send(self, data):
        headers = {
            "Authorization": f"Splunk {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "event": data
        }
        response = requests.post(self.splunk_url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
