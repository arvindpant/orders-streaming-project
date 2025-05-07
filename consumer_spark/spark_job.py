from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType
import avro.schema
import avro.io
import io
import requests
import json

# Start Spark
spark = SparkSession.builder \
    .appName("ParquetWriter") \
    .getOrCreate()

# Load schema from Schema Registry
SCHEMA_REGISTRY_URL = "http://localhost:8086"
subject = "orders-value"
response = requests.get(f"{SCHEMA_REGISTRY_URL}/subjects/{subject}/versions/latest")
schema_str = response.json()['schema']
schema = avro.schema.parse(schema_str)

# Decode Avro using Python
def decode_confluent_avro(avro_bytes):
    if avro_bytes is None:
        return None
    try:
        bytes_io = io.BytesIO(avro_bytes)
        bytes_io.read(5)  # skip magic byte + 4-byte schema ID
        decoder = avro.io.BinaryDecoder(bytes_io)
        reader = avro.io.DatumReader(schema)
        decoded = reader.read(decoder)
        return json.dumps(decoded)  # or return decoded['order_id'] etc.
    except Exception as e:
        return None

decode_udf = udf(decode_confluent_avro, StringType())

# Read Kafka
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "latest") \
    .load()

# Decode
decoded_df = df_kafka.withColumn("decoded", decode_udf(col("value")))

# Print to console
# query = decoded_df.select("decoded").writeStream \
#     .format("console") \
#     .option("truncate", False) \
#     .start()

# Write streaming data to Parquet
query = decoded_df.writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option("path", "data/streaming_parquet_output") \
    .option("checkpointLocation", "data/checkpoint_dir") \
    .start()

query.awaitTermination()

