# Databricks notebook source
# Objective: Provide a df containing 'order_id' and 'contact_full_name' that must contain the full name of the contact. In case this information is not available, the placeholder "John Doe" should be utilized.

import re
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import sys
sys.path.insert(0, "/Workspace/IFCO_Challenge/src")
from transformations import get_full_name

import urllib.request

BASE_URL = "https://raw.githubusercontent.com/smoyacopa/ifco-data-challenge/main/data"

urllib.request.urlretrieve(f"{BASE_URL}/orders.csv", "/tmp/orders.csv")
urllib.request.urlretrieve(f"{BASE_URL}/invoicing_data.json", "/tmp/invoicing_data.json")

ORDERS_PATH     = "file:///tmp/orders.csv"
INVOICING_PATH  = "file:///tmp/invoicing_data.json"

spark = SparkSession.builder.getOrCreate()
 
ORDERS_PATH     = "/Volumes/workspace/ifco_test/ifco_resources/orders.csv"
INVOICING_PATH  = "/Volumes/workspace/ifco_test/ifco_resources/invoicing_data.json"

df_orders_raw = (
    spark.read
    .option("header", "true")
    .option("sep", ";")
    .option("escape", '"')
    .csv(ORDERS_PATH)
)

# COMMAND ----------


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