




import os
import pathlib
from secrets import choice

os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"
os.environ["PYSPARK_PYTHON"] = r"C:\Users\ellip\AppData\Local\Programs\Python\Python310\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\ellip\AppData\Local\Programs\Python\Python310\python.exe"

from numpy import true_divide
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count

spark = (
    SparkSession.builder
    .master("local[*]")
    .config("spark.driver.host", "localhost")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .appName("Group By Example")
    .getOrCreate()
)



"""
Oracle Tables
        ↓
CSV Files
        ↓
Parquet Files
        ↓
Delta Lake
        ↓
Databricks
 """

df = (
    spark.read
         .option("header", "true")
         .csv("data/employees.csv")
)
clean_df = df.dropna()  #  return new DataFrame with all rows containing null values removed , only the columns that are not null will be kept , in memory, the original df is not modified
print("Count of cleaned DataFrame:", clean_df.count())
print("Count of original DataFrame:", df.count())

"""
now let s attack Parquet files, which are columnar storage files that are more efficient than CSV files. Parquet files are also self-describing, meaning they contain metadata about the schema of the data they contain. This makes them a good choice for storing large datasets that will be queried frequently. """

# save the cleaned DataFrame as a Parquet file
clean_df.write.mode("overwrite").parquet(
    "data/employees_parquet"
)
import pathlib
print("Parquet file saved successfully.in the data/employees_parquet directory.", pathlib.Path("data/employees_parquet").resolve())
