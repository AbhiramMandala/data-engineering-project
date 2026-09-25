# Task 4: reproducible ingestion container
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY scripts/ ./scripts/
COPY logs/ ./logs/
CMD ["python", "scripts/fetch_api.py"]
