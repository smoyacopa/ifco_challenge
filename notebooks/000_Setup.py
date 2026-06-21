# Databricks notebook source
import urllib.request
from pyspark.sql import functions as F
import sys

BASE_URL = "https://raw.githubusercontent.com/smoyacopa/ifco_challenge/main/data"
NOTEBOOK_PATH = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
REPO_ROOT = "/" + "/".join(NOTEBOOK_PATH.strip("/").split("/")[:-1])
sys.path.insert(0, f"{REPO_ROOT}/src")

urllib.request.urlretrieve(f"{BASE_URL}/orders.csv", "/tmp/orders.csv")
urllib.request.urlretrieve(f"{BASE_URL}/invoicing_data.json", "/tmp/invoicing_data.json")

ORDERS_PATH     = "file:///tmp/orders.csv"
INVOICING_PATH  = "file:///tmp/invoicing_data.json"

print("Setup completed")
print(f" ORDERS_PATH: {ORDERS_PATH}")
print(f" INVOICING_PATH:{INVOICING_PATH}")