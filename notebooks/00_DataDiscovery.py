# Databricks notebook source
# MAGIC %run ./000_Setup

# COMMAND ----------

# Objetive: To undestand the structure, quality and quirks of the two files before solving the exercises

# Files:
# orders.csv --> factual information regarding the orders received
# invoicing_data.json --> invoices for each order

import json
import re
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------

# After manual inspection of the csv --> headers, separator and quote/escape characters identified  
df_orders_raw = spark.read \
    .option("header", "true") \
    .option("sep", ";") \
    .option("quote", '"') \
    .option("escape", '"') \
    .csv(ORDERS_PATH)

df_orders_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC Discoveries 
# MAGIC - Date as string

# COMMAND ----------

# Format of the date field
df_orders_raw.select("date").distinct().orderBy("date").show(20)


# COMMAND ----------

# MAGIC %md
# MAGIC Discoveries
# MAGIC - Format DD.MM.YY (ej. "29.01.22") → will be parsed like so 
# MAGIC - Range: 2021-2025.

# COMMAND ----------


# After manual inspection of the json --> multiline
df_invoices_raw = spark.read \
    .option("multiline", "true") \
    .json(INVOICING_PATH)

# Aplanar
df_invoices = df_invoices_raw \
    .select(F.explode("data.invoices").alias("inv")) \
    .select("inv.*")

df_invoices.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC Discovery
# MAGIC --> grossValue, vat as strings

# COMMAND ----------

# Counts
n_orders    = df_orders_raw.count()
n_invoices  = df_invoices.count()
n_cols_ord  = len(df_orders_raw.columns)
n_cols_inv  = len(df_invoices.columns)
 
print(f"\n[orders]    {n_orders} filas  × {n_cols_ord} columnas")
print(f"[invoices] {n_invoices} filas  × {n_cols_inv} columnas")

# COMMAND ----------

# MAGIC %md
# MAGIC Discovery 
# MAGIC - Few invoices (~18% orders)

# COMMAND ----------

# Nulls & empties
def null_report(df, label):
    print(f"\n[{label}] Nulos y cadenas vacías:")
    exprs = [
        F.sum(
            (F.col(c).isNull() | (F.trim(F.col(c)) == "")).cast("int")
        ).alias(c)
        for c in df.columns
    ]
    df.select(exprs).show(1, truncate=False)
 
null_report(df_orders_raw, "orders")
# HALLAZGOS esperados:
#   - contact_data: ~8 filas vacías/nulas  → placeholder "John Doe" / "Unknown"
#   - salesowners:  0 nulos (siempre hay al menos uno)
 
null_report(df_invoices, "invoicing")
# HALLAZGOS esperados: sin nulos en los campos clave

# COMMAND ----------

# MAGIC %md
# MAGIC Discovery
# MAGIC - Only nulls found in contact data, placeholder might be needed

# COMMAND ----------

# Duplicated order_id
print("\n[orders] duplicated IDs (order_id):")
dup_orders = df_orders_raw.groupBy("order_id") \
    .count() \
    .filter(F.col("count") > 1)
dup_orders.show(truncate=False)
 
 # Duplicated invoice_id
print("\n[invoicing] duplicated IDs (invoice_id):")
dup_inv_id = df_invoices.groupBy("id") \
    .count() \
    .filter(F.col("count") > 1)
dup_inv_id.show(truncate=False)
 
 # Duplicated order_id in invoices
print("\n[invoicing] Same order_id in multiple invoices:")
dup_order_inv = df_invoices.groupBy("orderId") \
    .count() \
    .filter(F.col("count") > 1)
dup_order_inv.show(truncate=False)


# COMMAND ----------

# MAGIC %md
# MAGIC Discoveries 
# MAGIC - Orders do not have duplicated IDs (order_id)
# MAGIC - Invoices do not have duplicated IDs (invoice_id)
# MAGIC - Invoices have one duplicated order_id

# COMMAND ----------

# We have to investigate if the duplicated order_ID comes from a duplicated line or it is a different issue
duplicated_ids = df_invoices.groupBy("order_id") \
    .count() \
    .filter(F.col("count") > 1) \
    .select("order_id")

# Rows with duplicated order_id
df_only_duplicates = df_orders_raw.join(duplicated_ids, on="order_id", how="inner")

# Compare with distinct
total_rows = df_only_duplicates.count()
distinct_rows = df_only_duplicates.distinct().count()

print("Result:")
if total_rows > distinct_rows and distinct_rows == duplicated_ids.count():
    print("Exact duplicates")
else:
    print("Not duplicates")


# COMMAND ----------

# MAGIC %md
# MAGIC