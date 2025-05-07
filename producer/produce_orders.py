# # =======================
# # producer/produce_orders.py
# # =======================

# import json
# import random
# import time
# from confluent_kafka import avro
# from confluent_kafka.avro import AvroProducer

# SCHEMA_REGISTRY_URL = "http://localhost:8086"
# KAFKA_BROKER = "localhost:9092"
# TOPIC = "orders"

# value_schema_str = open("producer/schema.avsc", "r").read()
# value_schema = avro.loads(value_schema_str)

# producer = AvroProducer(
#     {
#         'bootstrap.servers': KAFKA_BROKER,
#         'schema.registry.url': SCHEMA_REGISTRY_URL
#     },
#     default_value_schema=value_schema
# )

# statuses = ['CREATED', 'PAID', 'SHIPPED', 'CANCELLED']

# while True:
#     order = {
#         "order_id": f"order_{random.randint(1000, 9999)}",
#         "user_id": f"user_{random.randint(1, 100)}",
#         "amount": round(random.uniform(10.0, 500.0), 2),
#         "status": random.choice(statuses),
#         "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
#     }
#     producer.produce(topic=TOPIC, value=order)
#     print(f"Produced: {order}")
#     time.sleep(2)


from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer
import random, time, uuid

SCHEMA_REGISTRY_URL = "http://localhost:8086"
KAFKA_BROKER = "localhost:9092"
TOPIC = "orders"

# Avro schema
value_schema_str = """
{
  "type": "record",
  "name": "Order",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "user_id", "type": "string"},
    {"name": "amount", "type": "string"},
    {"name": "status", "type": "string"},
    {"name": "timestamp", "type": "string"}
  ]
}
"""

# Convert dict to object
def dict_to_order(obj, ctx):
    return obj

schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_serializer = AvroSerializer(
    schema_registry_client=schema_registry_client,
    schema_str=value_schema_str,
    to_dict=dict_to_order
)

producer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer
}

producer = SerializingProducer(producer_conf)

statuses = ['CREATED', 'PAID', 'SHIPPED', 'CANCELLED']

while True:
    order = {
        "order_id": f"order_{uuid.uuid4().hex[:8]}",
        "user_id": f"user_{random.randint(1, 100)}",
        "amount": str(round(random.uniform(10.0, 500.0), 2)),
        "status": random.choice(statuses),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

    producer.produce(topic=TOPIC, key=order["order_id"], value=order)
    print("Produced:", order)
    producer.flush()
    time.sleep(2)
