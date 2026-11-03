

import os

os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"
os.environ["PYSPARK_PYTHON"] = r"C:\Users\ellip\AppData\Local\Programs\Python\Python310\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\ellip\AppData\Local\Programs\Python\Python310\python.exe"

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


# employees
employees = [
    (1, "Abdul", 10),
    (2, "John", 20),
    (3, "Sarah", 10),
]

# departments
departments = [
    (10, "Database"),
    (20, "Development")
]

emp_df = spark.createDataFrame(
    employees,
    ["emp_id", "name", "dept_id"]
)

dept_df = spark.createDataFrame(
    departments,
    ["dept_id", "department_name"]
)

result = emp_df.join(
    dept_df,
    emp_df.dept_id == dept_df.dept_id,
    "inner"
)

result.show()



'''
Commit Your Progress

You're building a very nice learning repository now:

PowerShell
git add .
git commit -m "Completed PySpark group by / Spark SQL/Join  examples"
git push
'''
