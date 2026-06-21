# Databricks notebook source
# Objective: Calculate the distribution of crate types per company (number of orders per type). Ensure to include unit tests to validate the correctness of your calculations.

import json
import re
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import sys
sys.path.insert(0, "/Workspace/IFCO_Challenge/src")
from transformations import normalize_company_name, get_crate_distribution_by_company


spark = SparkSession.builder.getOrCreate()

# COMMAND ----------

df_orders_raw = (
    spark.read
    .option("header", "true")
    .option("sep", ";")
    .option("escape", '"')
    .csv(ORDERS_PATH)
)

# Company name normalization
# - lowercase
# - only letters
# - trim
normalize_company_name_udf = F.udf(normalize_company_name, StringType())

df_orders = df_orders_raw.withColumn(
    "company_name_clean",
    normalize_company_name_udf(df_orders_raw["company_name"])
)



# COMMAND ----------

# Call the transformation function directly (not as a UDF)
df_distribution = get_crate_distribution_by_company(df_orders)

df_distribution.show(truncate=False)