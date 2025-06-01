from kafka import KafkaConsumer
import json
from joblib import load
import pandas as pd
import os
from consumer.splunk_logger import SplunkLogger


class AIAnomalyDetector:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "..", "ai", "anomaly_model.joblib")
        self.model = load(model_path)
        print(f"Loaded model from {model_path}")

    def is_anomaly(self, data: dict) -> bool:
        X = pd.DataFrame([{
            "temperature": data["temperature"],
            "pressure": data["pressure"],
            "vibration": data["vibration"]
        }])
        prediction = self.model.predict(X)
        return prediction[0] == -1  # -1 = anomaly


class KafkaSensorConsumer:
    def __init__(self, topic: str, bootstrap_servers: str = "localhost:9092"):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="oil-detector-group"
        )
        self.detector = AIAnomalyDetector()
        self.splunk_logger = SplunkLogger(
            token="your-token dont use this in prod setup",
            splunk_url="http://localhost:8088/services/collector"
        )

    def listen(self):
        print(f"📡 Listening to Kafka topic: {self.topic}")
        for message in self.consumer:
            data = message.value
            if self.detector.is_anomaly(data):
                print(f"🚨 AI Anomaly Detected! {data}")
                self.splunk_logger.send(data)
            else:
                print(f"✅ Normal: {data}")


if __name__ == "__main__":
    consumer = KafkaSensorConsumer(topic="oil-sensor-data")
    consumer.listen()
