# Databricks notebook source
import re
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *


spark = SparkSession.builder.getOrCreate()
 
ORDERS_PATH     = "/Volumes/workspace/ifco_test/ifco_resources/orders.csv"
INVOICING_PATH  = "/Volumes/workspace/ifco_test/ifco_resources/invoicing_data.json"

# COMMAND ----------

# Typecasting applied after data discovery
df_invoices = (
    spark.read
    .option("multiLine", "true")
    .json("INVOICING_PATH")
    .select(F.explode("data.invoices").alias("inv"))
    .select(
        F.col("inv.id").alias("invoice_id"),
        F.col("inv.orderId").alias("order_id"),
        F.col("inv.grossValue").cast(IntegerType()).alias("gross_cents"),
        F.col("inv.vat").cast(DoubleType()).alias("vat_pct")
    )
)

# Using ROW_NUMBER to keep only one of the two duplicated lines (as discovered during the preliminar analysis)
df_invoices.createOrReplaceTempView("invoices")

df_invoices = spark.sql("""
    SELECT order_id, gross_cents, vat_pct
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY invoice_id) AS rn
        FROM invoices_raw
    )
    WHERE rn = 1
""")

# Custom transformation to obtain Net Value
net_value_udf = F.udf(calculate_net_value_eur, DoubleType())

df_invoices = df_invoices.withColumn(
    "net_value_eur",
    net_value_udf(F.col("gross_cents"), F.col("vat_pct"))
)

print(f"Unique Invoices: {df_invoices.count()}")
df_invoices.show(truncate=False)


# COMMAND ----------


# Sales Owners are placed in individual rows and their positions are captured

df_orders_raw = (
    spark.read
    .option("header", "true")
    .option("sep", ";")
    .option("escape", '"')
    .csv(ORDERS_PATH)
)

df_orders_raw.createOrReplaceTempView("orders_raw")

df_salesowners = spark.sql("""
    SELECT
        order_id,
        TRIM(owner)  AS salesowner,
        pos + 1   AS position   -- 1-indexed
    FROM orders_raw
    LATERAL VIEW POSEXPLODE(SPLIT(salesowners, ',')) t AS pos, owner
    WHERE TRIM(owner) != ''
""")

df_salesowners.show(20, truncate=False)

 # Join orders - invoices and comissions calculation calcular comissions

commission_rate_udf = F.udf(get_commission_rate, DoubleType())

df_commissions = (
    df_salesowners
    .join(df_invoices, on="order_id", how="inner")  # solo órdenes con factura
    .withColumn("commission_rate", commission_rate_udf(F.col("position")))
    .withColumn(
        "commission_eur",
        F.round(F.col("net_value_eur") * F.col("commission_rate"), 2)
    )
)

## Group by salesowner and order

result = (
    df_commissions
    .groupBy("salesowner")
    .agg(F.round(F.sum("commission_eur"), 2).alias("total_commission_eur"))
    .filter(F.col("total_commission_eur") > 0)  # excluimos los que no cobran
    .orderBy(F.desc("total_commission_eur"))
)

result.show(truncate=False)