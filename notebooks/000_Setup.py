# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "2"
# ///
# Databricks notebook source
import sys

NOTEBOOK_PATH = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
REPO_ROOT = "/" + "/".join(NOTEBOOK_PATH.strip("/").split("/")[:-2])
sys.path.insert(0, f"/Workspace{REPO_ROOT}/src")

ORDERS_PATH    = f"/Workspace{REPO_ROOT}/data/orders.csv"
INVOICING_PATH = f"/Workspace{REPO_ROOT}/data/invoicing_data.json"

print("Setup completed")
print(f"  REPO_ROOT:      {REPO_ROOT}")
print(f"  ORDERS_PATH:    {ORDERS_PATH}")
print(f"  INVOICING_PATH: {INVOICING_PATH}")