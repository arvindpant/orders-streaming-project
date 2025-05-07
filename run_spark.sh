# #!/bin/bash

# SPARK_SUBMIT=${SPARK_SUBMIT:-spark-submit}

# # Required dependencies
# PACKAGES=(
#   org.apache.spark:spark-avro_2.12:3.3.1
#   io.delta:delta-core_2.12:2.1.0
#   io.confluent:kafka-schema-registry-client:7.3.0
#   io.confluent:kafka-avro-serializer:7.3.0
#   io.delta:delta-core_2.12:3.0.0
# io.delta:delta-storage:3.0.0

#   org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0
# )

# # Maven repo for Confluent
# CONFLUENT_REPO=https://repo.maven.apache.org/maven2

# PACKAGE_CSV=$(IFS=, ; echo "${PACKAGES[*]}")

# $SPARK_SUBMIT \
#   --packages "$PACKAGE_CSV" \
#   --repositories "$CONFLUENT_REPO" \
#   --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
#   --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
#   consumer_spark/spark_job.py

#!/bin/bash

PACKAGES=(
  org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1
  org.apache.spark:spark-avro_2.12:3.4.1
  io.delta:delta-core_2.12:1.2.1
  io.delta:delta-storage:1.2.1
  io.confluent:kafka-schema-registry-client:7.2.1
  io.confluent:kafka-avro-serializer:7.2.1
  org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.4.1
)

PACKAGE_CSV=$(IFS=, ; echo "${PACKAGES[*]}")

spark-submit \
  --jars "/jars/delta-core_2.12-1.2.1.jar,/jars/delta-storage-1.2.1.jar" \
  --packages "$PACKAGE_CSV" \
  --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
  --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
  --conf "spark.delta.logStore.class=org.apache.spark.sql.delta.storage.S3SingleDriverLogStore" \
  consumer_spark/spark_job.py