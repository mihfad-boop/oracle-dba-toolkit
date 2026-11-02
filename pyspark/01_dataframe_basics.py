

from pyspark.sql import SparkSession
'''
spark = SparkSession.builder.appName(
    "DBA Learning"
).getOrCreate()
'''
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("DBA Learning")
    .getOrCreate()
)


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
