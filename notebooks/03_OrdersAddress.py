# Databricks notebook source
# MAGIC %run ./000_Setup

# COMMAND ----------

# Objective: Provide a df containing 'order_id' and 'contact_address' that should adhere to the following information and format: "city name, postal code". If the city name is not available, the placeholder "Unknown" should be used. If the postal code is not known, the placeholder "UNK00" should be used.

import re
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import sys
from transformations import get_address

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
get_address_udf = F.udf(get_address, StringType())

df_2 = (
    df_orders_raw
    .withColumn("contact_address", get_address_udf(F.col("contact_data")))
    .select("order_id", "contact_address")
)

df_2.show(truncate=False)

# Quick count check
total    = df_2.count()
nulos    = df_2.filter(F.col("contact_address").isNull()).count()
unknown  = df_2.filter(F.col("contact_address").startswith("Unknown")).count()
unk00    = df_2.filter(F.col("contact_address").endswith("UNK00")).count()

print(f"Total count:{total}")
print(f"Null adress count:{nulos}")
print(f"City placeholder count: {unknown}")
print(f"CP placeholder count: {unk00}")

# COMMAND ----------

# Guardamos en Unity Catalog
df_2.write \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .format("delta") \
    .saveAsTable("workspace.ifco_test.address")