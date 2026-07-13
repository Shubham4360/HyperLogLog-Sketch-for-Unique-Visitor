from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType

from database.postgres import PostgreSQL
from consumer.hll_counter import HyperLogLog
from consumer.exact_counter import ExactCounter
from config.settings import *
import plotly.express as px





# -----------------------------
# Database
# -----------------------------
database = PostgreSQL()

# -----------------------------
# Kafka Schema
# -----------------------------
schema = (
    StructType()
    .add("event_id", StringType())
    .add("event_type", StringType())
    .add("user_id", StringType())
    .add("username", StringType())
    .add("repo", StringType())
    .add("created_at", StringType())
)

# -----------------------------
# HyperLogLog + Exact Counter
# -----------------------------
hll = HyperLogLog(HLL_PRECISION)
exact = ExactCounter()
event_counter = 0


def process_batch(dataframe, batch_id):
    global event_counter

    rows = dataframe.collect()

    print(f"Batch {batch_id}: Received {len(rows)} rows")

    for row in rows:
        if row.user_id:
            hll.add(row.user_id)
            exact.add(row.user_id)
            event_counter += 1

    exact_count = exact.count()
    hll_count = hll.count()

    error = abs(exact_count - hll_count) / max(exact_count, 1)
    memory_usage = len(hll.registers)

    database.insert_metrics(
        events_processed=event_counter,
        exact_users=exact_count,
        hll_users=hll_count,
        error_percentage=round(error * 100, 4),
        memory_usage_bytes=memory_usage
    )

    print("==========================")
    print("Batch:", batch_id)
    print("Events:", event_counter)
    print("Exact:", exact_count)
    print("HLL:", hll_count)
    print("Error:", round(error * 100, 4), "%")
    print("Memory Usage:", memory_usage)
    print("==========================")


def main():
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("GitHub-HyperLogLog")
        .config(
            "spark.jars.packages",
            ",".join([
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1",
                "org.apache.kafka:kafka-clients:3.5.1"
            ])
        )    
        .config("spark.sql.shuffle.partitions", "2")   
        .getOrCreate()
    )

    stream = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets", "latest")
        .load()
    )

    events = (
        stream
        .selectExpr("CAST(value AS STRING)")
        .select(from_json(col("value"), schema).alias("data"))
        .select("data.*")
    )

    query = (
        events
        .writeStream
        .foreachBatch(process_batch)
        .trigger(processingTime="5 seconds")
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
    