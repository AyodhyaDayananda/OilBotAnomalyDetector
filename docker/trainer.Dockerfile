FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ai/model_trainer.py .
COPY producer/training_data.parquet ./producer/training_data.parquet
CMD ["python", "model_trainer.py"]
