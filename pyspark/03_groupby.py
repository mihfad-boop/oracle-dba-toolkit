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

# Group by department and calculate average salary and employee count
df.groupBy("department").agg(
    avg("salary").alias("avg_salary"),
    count("*").alias("employees")
).show()

# Order by salary in descending order
df.orderBy(df.salary.desc()).show()

# SQL inside Spark
df.createOrReplaceTempView("v_employees")
spark.sql("""
SELECT department,
       AVG(salary) avg_salary
FROM v_employees
GROUP BY department
""").show()

spark.stop()

'''
as reminder
What you've learned so far
Oracle SQL	PySpark
---------   ----------
SELECT	    select()
WHERE	    filter()
GROUP BY	groupBy()
COUNT(*)	count()
AVG()   	avg()
ORDER BY	orderBy()
VIEW	    createOrReplaceTempView()
SQL Query	spark.sql()

'''
'''
Exactly! 👍

As an Oracle DBA, the best analogy is:

df.createOrReplaceTempView("v_employees")


is similar to:

CREATE OR REPLACE VIEW v_employees AS
SELECT *
FROM employees;


But with one important difference:

Oracle View

Stored in the database:

CREATE OR REPLACE VIEW v_employees AS
SELECT *
FROM employees;

Persistent
Exists after you disconnect
Visible to other users (subject to permissions)
Spark Temporary View

Created in memory:

df.createOrReplaceTempView("v_employees")

Exists only in the current Spark session
Not written to disk
Not stored in a database
Disappears when the Spark session ends
What's actually happening?

You create a DataFrame:

df = spark.createDataFrame(
    data,
    ["id", "name", "department", "salary"]
)


Then:

df.createOrReplaceTempView("v_employees")


registers that DataFrame under a SQL name:

v_employees
    ↓
points to
    ↓
df


So now both are references to the same underlying data:

df.show()


and

spark.sql("SELECT * FROM v_employees").show()


return the same rows.

Think of it like an alias

Before:

DataFrame
   |
   └── df


After:

DataFrame
   |
   ├── df
   |
   └── v_employees


df is the Python reference.

v_employees is the SQL reference.

Example
df.createOrReplaceTempView("v_employees")

spark.sql("""
SELECT *
FROM v_employees
WHERE department = 'DBA'
""").show()


As an Oracle DBA, you'll probably like this approach because you can write almost pure SQL.

Even more Oracle-like

You can mix DataFrames and SQL:

df.createOrReplaceTempView("v_employees")

result = spark.sql("""
SELECT department,
       AVG(salary) avg_salary
FROM v_employees
GROUP BY department
""")

result.show()


Notice:

SQL Query
      ↓
returns
      ↓
DataFrame


That's a key Spark concept:

DataFrame  ←→  SQL View


You can switch between them freely.

Rule of thumb

Whenever you see:

createOrReplaceTempView()


think:

"Create a temporary SQL view name for this DataFrame so I can query it using SQL."

That's exactly how many Data Engineers who come from Oracle, SQL Server, and PostgreSQL backgrounds work in Spark and Databricks. 🚀


'''
