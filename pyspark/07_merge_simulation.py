

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

employees_df = (
    spark.read
         .option("header","true")
         .option("inferSchema","true")
         .csv("data/employees.csv")
)

'''
3  -> salary changed
50 -> salary changed
100 -> salary changed
101 -> new employee
'''
updates_df = (
    spark.read
         .option("header","true")
         .option("inferSchema","true")
         .csv("data/employees_updates.csv")
)


employees_df.show()
updates_df.show()


'''
Step 3

Find matching rows.

Equivalent Oracle:

SQL
SELECT *
FROM employees e
JOIN updates u
ON e.emp_id = u.emp_id;
'''



matches = (
    employees_df.alias("e")
    .join(
        updates_df.alias("u"),
        "emp_id"
    )
)

matches.show()


'''
+------+-----+----------+------+---------+-----+----------+------+---------+
|emp_id| name|department|salary|     city| name|department|salary|     city|
+------+-----+----------+------+---------+-----+----------+------+---------+
|     3|Sarah|       DBA| 95000| Montreal|Sarah|       DBA| 98000| Montreal|
|    50| Levi|        HR| 78500|Vancouver| Levi|        HR| 80000|Vancouver|
+------+-----+----------+------+---------+-----+----------+------+---------+
'''



'''
Step 4

Find new rows.
'
'''
new_rows = (
    updates_df.alias("u")
    .join(
        employees_df.alias("e"),
        "emp_id",
        "left_anti"
    )
)

new_rows.show()
'''
+------+------+----------+------+--------+
|emp_id|  name|department|salary|    city|
+------+------+----------+------+--------+
|   100|Robert|       DEV| 92000| Toronto|
|   101| Kevin|       DBA| 95000|Montreal|
+------+------+----------+------+--------+

'''
