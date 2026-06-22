# Databricks notebook source
# MAGIC %run ./000_Setup

# COMMAND ----------

# Objective: Provide a df containing 'order_id' and 'contact_full_name' that must contain the full name of the contact. In case this information is not available, the placeholder "John Doe" should be utilized.

import re
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import sys
from transformations import get_full_name

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------


df_orders_raw = (
    spark.read
    .option("header", "true")
    .option("sep", ";")
    .option("escape", '"')
    .csv(ORDERS_PATH)
)

# Custom function is used to apply the transformations
get_full_name_udf = F.udf(get_full_name, StringType())

df_1 = (
    df_orders_raw
    .withColumn("contact_full_name", get_full_name_udf(F.col("contact_data")))
    .select("order_id", "contact_full_name")
)

df_1.show(truncate=False)

# Quick count check
total = df_1.count()
john_doe = df_1.filter(F.col("contact_full_name") == "John Doe").count()
nulls = df_1.filter(F.col("contact_full_name").isNull()).count()

print(f"Total orders:{total}")
print(f"Placeholder count:{john_doe}")
print(f"Placeholder count:{nulls}")