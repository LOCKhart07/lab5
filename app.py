from pyspark.sql.functions import col, from_json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DecimalType

import os, sys

import env_variables


os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


# Define the schema for the JSON data
# {'frame_number': frame_nmr, 'license_plates': texts}
json_schema = StructType(
    [
        StructField("frame_number", DecimalType(), True),
        StructField("license_plates", StringType(), True),
    ]
)

# fmt:off
# Create a SparkSession
spark = (
    SparkSession.builder.config("spark.driver.host", env_variables.SPARK_DRIVER_HOST)
    .config("spark.kubernetes.container.image", env_variables.SPARK_KUBERNETES_CONTAINER_IMAGE)
    .config("spark.kubernetes.driver.master", env_variables.SPARK_KUBERNETES_DRIVER_MASTER)
    .config("spark.kubernetes.driver.pod.name", env_variables.SPARK_KUBERNETES_DRIVER_POD_NAME)
    .config("spark.driver.port", env_variables.SPARK_DRIVER_PORT)
    .config("spark.kubernetes.authenticate.driver.serviceAccountName", env_variables.SPARK_KUBERNETES_AUTHENTICATE_DRIVER_SERVICE_ACCOUNT_NAME)
    .config("spark.kubernetes.executor.podNamePrefix", env_variables.SPARK_KUBERNETES_EXECUTOR_PODNAMEPREFIX)
    .config("spark.executor.instances", env_variables.SPARK_EXECUTOR_CORES)
    .config("spark.executor.cores", env_variables.SPARK_EXECUTOR_CORES)
    .config("spark.executor.memory", env_variables.SPARK_EXECUTOR_MEMORY)
    .appName("Kafka to PostgreSQL")
    .getOrCreate()
)
# fmt:on

# Create a Structured Streaming query
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", env_variables.KAFKA_BOOTSTRAP_SERVER)
    .option("subscribe", env_variables.KAFKA_READ_TOPIC)
    .option("startingOffsets", "latest")
    .load()
    .select(from_json(col("value").cast("string"), json_schema).alias("parsed_value"))
    .select(col("parsed_value.*"))
)


def process_batches(df, epoch_id):
    (
        df.write.format("jdbc")
        .mode("append")
        .option("url", env_variables.POSTGRES_URL)
        .option("dbtable", "license_plates")
        .option("user", env_variables.POSTGRES_USERNAME)
        .option("password", env_variables.POSTGRES_PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .save()
    )
    print("data loaded")


query = (
    df.writeStream.foreachBatch(process_batches)
    .outputMode("append")
    .start()
    .awaitTermination()
)

query.awaitTermination()
