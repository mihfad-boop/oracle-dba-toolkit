import os

os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"

os.environ["PYSPARK_PYTHON"] = r"C:\Users\ellip\AppData\Local\Programs\Python\Python310\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\ellip\AppData\Local\Programs\Python\Python310\python.exe"

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .config("spark.driver.host", "localhost")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .appName("PySpark Test")
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
