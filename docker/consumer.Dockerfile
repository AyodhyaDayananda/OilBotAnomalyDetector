FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY consumer/anomaly_detector.py .
COPY ai/anomaly_model.joblib ./ai/anomaly_model.joblib
CMD ["python", "anomaly_detector.py"]
