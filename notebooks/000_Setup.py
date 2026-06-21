# Databricks notebook source
# 00_Setup.py
import urllib.request
from pyspark.sql import functions as F
import sys

BASE_URL = "https://raw.githubusercontent.com/tu-smoyacopa/ifco_challenge/main/data"

urllib.request.urlretrieve(f"{BASE_URL}/orders.csv", "/tmp/orders.csv")
urllib.request.urlretrieve(f"{BASE_URL}/invoicing_data.json", "/tmp/invoicing_data.json")

ORDERS_PATH     = "file:///tmp/orders.csv"
INVOICING_PATH  = "file:///tmp/invoicing_data.json"

sys.path.insert(0, "/Workspace/IFCO_Challenge/src")

print("Setup completes")
print(f"   ORDERS_PATH:     {ORDERS_PATH}")
print(f"   INVOICING_PATH:  {INVOICING_PATH}")