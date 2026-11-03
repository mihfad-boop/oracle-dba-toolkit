

import os

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

df = (
    spark.read
         .option("header", "true")
         .csv("data/employees.csv")
)
print("Row count =", df.count())
df.show()
print("Row count all ")
df.show(100, truncate=True)

'''
Show rows without truncation
For longer text columns:
Python
df.show(100, truncate=False)

in addition:
Imagine accidentally doing:

Python
df.show(100000000)

on a huge Databricks table 😄

That's why Spark defaults to:

Python
show(20)

for safety.


'''
df.printSchema()
'''root
 |-- emp_id: string (nullable = true)
 |-- name: string (nullable = true)
 |-- department: string (nullable = true)
 |-- salary: string (nullable = true)
 |-- city: string (nullable = true)
'''
df.groupBy("department").count().show()
'''
+----------+-----+
|department|count|
+----------+-----+
|        HR|   25|
|       DEV|   26|
|       DBA|   26|
+----------+-----+
'''
#Average salary by department
from pyspark.sql.functions import avg

df.groupBy("department") \
  .agg(avg("salary").alias("avg_salary")) \
  .show()

'''
+----------+-----------------+
|department|       avg_salary|
+----------+-----------------+
|        HR|77270.83333333333|
|       DEV|86865.38461538461|
|       DBA|92923.07692307692|
+----------+-----------------+
'''
#Count by city
#Python
df.groupBy("city").count().show()



#ETCH FIRST 10 ROWS ONLY;  in oracle but df.show(10)    || note  df.show()  fetches 20 rows by default

df.printSchema()
print("Rows:", df.count())
df.show(10)


'''
Next Topic: Data Quality & Data Cleaning

Before Databricks, every Data Engineer must know how to find:

NULL values
Bad records
Missing data
Invalid formats
Duplicates
'''

'''
Lesson 6 - Data Profiling


'''
from pyspark.sql.functions import col

print("Showing salary null values:")
print("Showing how many null values:",df.filter(col("salary").isNull()).count())
#ount Missing Salaries
print(df.filter(col("salary").isNull()).count())
df.filter(col("salary").isNull()).show()


# Find Bad Records
# Python

df.filter(
col("city").isNull()
).show()


""" Remove Bad Records
Python """
clean_df = df.dropna()  #  return new DataFrame with all rows containing null values removed , only the columns that are not null will be kept , in memory, the original df is not modified
print(clean_df.count())




"""
Lesson 7 - Schema Inference

Notice your schema:

Plain Text
salary: string

Salary should really be numeric.

Currently Spark sees:

Plain Text
90000
85000
 """


# Instead read CSV with schema inference:  SALARY column will be numeric instead of string automatically
df = (
    spark.read
         .option("header","true")
         .option("inferSchema","true")
         .csv("data/employees.csv")
)
df.printSchema()



""" Lesson 8 - Aggregation Challenge

Try these yourself.

Average salary by city """
df.groupBy("city") \
  .agg(avg("salary").alias("avg_salary")) \
  .show()


# Highest salary
from pyspark.sql.functions import max
print("Showing highest salary:")
df.select(
    max("salary")
).show()


""" Highest-paid employee
Python """
print("Showing 3 highest-paid employees:")
df.orderBy(
df.salary.desc()
).show(3, truncate=False)


