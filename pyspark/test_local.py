# pyspark/test_local.py

import os

os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("PySpark Test")
    .config("spark.driver.host", "localhost")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
)

print("Spark Started Successfully")

data = [
    (1, "Oracle"),
    (2, "GoldenGate"),
    (3, "Databricks")
]

df = spark.createDataFrame(
    data,
    ["id", "technology"]
)

df.show()

spark.stop()
