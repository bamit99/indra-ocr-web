FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENV HF_HOME=/data/hf
EXPOSE 8310
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8310", "--workers", "1"]