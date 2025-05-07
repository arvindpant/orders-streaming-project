# Spark Streaming Orders Pipeline

This project demonstrates a real-time order streaming pipeline using Kafka, Confluent Schema Registry, Spark Structured Streaming, Flink, Apache Pinot, and Streamlit. Everything runs locally with Docker Compose.

---

## 🧱 Components

- **Producer (Python)**: Generates fake order data and pushes to Kafka (Avro-encoded).
- **Confluent Kafka**: Kafka + Schema Registry for Avro serialization.
- **Confluent Schema Registry.
- **Spark Structured Streaming (PySpark)**: Consumes Kafka data and writes to Delta Lake.
- **Streamlit**: Displays visual insights from the Delta Lake or Pinot backend.

---

## ▶️ How to Run

### 1. Setup Virtualenv
```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

docker compose up -d
docker compose down -v
docker compose up --build
