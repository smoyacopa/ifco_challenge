# Databricks notebook source
# MAGIC %run ./000_Setup

# COMMAND ----------

import re
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
from transformations import normalize_company_name


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
df_orders = df_orders_raw.withColumn(
    "company_name_clean",
    F.trim(F.regexp_replace(F.lower(F.col("company_name")), r"[^a-z0-9 ]", ""))
)


# Invoices
df_invoices_raw = (
    spark.read
    .option("multiLine", "true")
    .json(INVOICING_PATH)
    .select(F.explode("data.invoices").alias("inv"))
    .select(
        F.col("inv.id").alias("invoice_id"),
        F.col("inv.orderId").alias("order_id"),
        F.col("inv.grossValue").cast(IntegerType()).alias("gross_cents"),
        F.col("inv.vat").cast(DoubleType()).alias("vat_pct")
    )
)

# Using ROW_NUMBER to keep only one of the two duplicated lines (as discovered during the preliminar analysis)
df_invoices_raw.createOrReplaceTempView("invoices_raw")

df_invoices = spark.sql("""
    SELECT order_id, gross_cents, vat_pct
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY invoice_id) AS rn
        FROM invoices_raw
    )
    WHERE rn = 1
""")

# COMMAND ----------

# Exploded salesowners y recopilar únicos por empresa

df_orders.createOrReplaceTempView("orders")

owners = spark.sql("""
    WITH owners_exploded AS (
        SELECT
            company_name_clean,
            FIRST(company_name) OVER (
                PARTITION BY company_name_clean
                ORDER BY LENGTH(company_name) DESC
            ) AS company_name_canonical,
            TRIM(owner) AS salesowner
        FROM orders
        LATERAL VIEW EXPLODE(SPLIT(salesowners, ',')) t AS owner
        WHERE TRIM(owner) != ''
    )
    SELECT
        company_name_canonical AS company_name,
        company_name_clean,
        CONCAT_WS(', ', SORT_ARRAY(
            COLLECT_SET(salesowner)
        )) AS salesowners
    FROM owners_exploded
    GROUP BY
        company_name_canonical,
        company_name_clean
    ORDER BY
        company_name_clean
""")

owners.show(truncate=False)