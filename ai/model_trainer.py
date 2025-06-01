import pandas as pd
from sklearn.ensemble import IsolationForest
from joblib import dump


class AnomalyModelTrainer:
    def __init__(self, data_path: str = "producer/training_data.parquet", model_path: str = "ai/anomaly_model.joblib"):
        self.data_path = data_path
        self.model_path = model_path
        self.model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

    def load_data(self):
        df = pd.read_parquet(self.data_path)
        self.X = df[["temperature", "pressure", "vibration"]]
        print(f"📥 Loaded {len(df)} training records from Parquet.")

    def train_model(self):
        self.model.fit(self.X)
        print("🧠 Model training complete.")

    def save_model(self):
        dump(self.model, self.model_path)
        print(f"💾 Model saved to {self.model_path}")

    def run(self):
        self.load_data()
        self.train_model()
        self.save_model()


if __name__ == "__main__":
    trainer = AnomalyModelTrainer()
    trainer.run()
