import pandas as pd
from sensor_simulator import OilSensor


class TrainingDataCollector:
    def __init__(self, sensor_id: str, well_name: str, output_path: str = "producer/training_data.parquet", sample_size: int = 1000):
        self.sensor = OilSensor(sensor_id, well_name)
        self.output_path = output_path
        self.sample_size = sample_size
        self.data = []

    def generate_data(self):
        print(f"📊 Generating {self.sample_size} training samples...")
        for _ in range(self.sample_size):
            reading = self.sensor.generate_reading()
            self.data.append(reading)
        print("✅ Data generation complete.")

    def save_to_parquet(self):
        df = pd.DataFrame(self.data)
        df.to_parquet(self.output_path, index=False)
        print(f"💾 Saved training data to {self.output_path}")

    def run(self):
        self.generate_data()
        self.save_to_parquet()


if __name__ == "__main__":
    collector = TrainingDataCollector(
        sensor_id="TRAIN-SENSOR-001",
        well_name="Train-Well",
        output_path="training_data.parquet"
    )
    collector.run()
