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
    .appName("SQL Operations")
    .getOrCreate()
)

data = [
    (1, "Abdul", "DBA", 90000),
    (2, "John", "DEV", 85000),
    (3, "Sarah", "DBA", 95000),
    (4, "Mike", "DEV", 80000),
]

df = spark.createDataFrame(
    data,
    ["id", "name", "department", "salary"]
)

print("Original Data")
df.show()

print("DBAs Only")
df.filter(df.department == "DBA").show()

print("Names and Salaries")
df.select("name", "salary").show()

spark.stop()
