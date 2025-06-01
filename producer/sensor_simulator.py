import random
import time
from datetime import datetime
import json
from kafka import KafkaProducer


class OilSensor:
    def __init__(self, sensor_id: str, location: str):
        self.sensor_id = sensor_id
        self.location = location

    def read_temperature(self):
        return round(random.uniform(40, 90), 2)

    def read_pressure(self):
        return round(random.uniform(100, 300), 2)

    def read_vibration(self):
        return round(random.uniform(0.1, 5.0), 2)

    def generate_reading(self):
        return {
            "sensor_id": self.sensor_id,
            "location": self.location,
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": self.read_temperature(),
            "pressure": self.read_pressure(),
            "vibration": self.read_vibration()
        }


class SensorKafkaProducer:
    def __init__(self, topic, sensor, delay=1):
        self.topic = topic
        self.sensor = sensor
        self.delay = delay
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def stream_data(self):
        while True:
            data = self.sensor.generate_reading()
            print(f"📤 Sending to Kafka: {data}")
            self.producer.send(self.topic, value=data)
            time.sleep(self.delay)


if __name__ == "__main__":
    sensor = OilSensor(sensor_id="SENSOR-001", location="Well-Alpha")
    producer = SensorKafkaProducer(topic="oil-sensor-data", sensor=sensor)
    producer.stream_data()
