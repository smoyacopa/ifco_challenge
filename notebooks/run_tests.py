# Databricks notebook source
# MAGIC %sh
# MAGIC cd /Workspace/IFCO_Challenge
# MAGIC
# MAGIC # TESTS 01
# MAGIC # Le inyectamos la ruta absoluta al PYTHONPATH para que encuentre 'src'
# MAGIC export PYTHONPATH="/Workspace/IFCO_Challenge"
# MAGIC
# MAGIC # Ejecutamos apagando los bytes y moviendo la caché a /tmp
# MAGIC PYTHONDONTWRITEBYTECODE=1 pytest tests/test_01.py -v -o cache_dir=/tmp/.pytest_cache

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /Workspace/IFCO_Challenge
# MAGIC
# MAGIC # TESTS 02
# MAGIC export PYTHONPATH="/Workspace/IFCO_Challenge"
# MAGIC
# MAGIC PYTHONDONTWRITEBYTECODE=1 pytest tests/test_02.py -v -o cache_dir=/tmp/.pytest_cache

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /Workspace/IFCO_Challenge
# MAGIC
# MAGIC # TESTS 03
# MAGIC export PYTHONPATH="/Workspace/IFCO_Challenge"
# MAGIC
# MAGIC PYTHONDONTWRITEBYTECODE=1 pytest tests/test_03.py -v -o cache_dir=/tmp/.pytest_cache

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /Workspace/IFCO_Challenge
# MAGIC
# MAGIC # TESTS 04
# MAGIC export PYTHONPATH="/Workspace/IFCO_Challenge"
# MAGIC
# MAGIC PYTHONDONTWRITEBYTECODE=1 pytest tests/test_04.py -v -o cache_dir=/tmp/.pytest_cache

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /Workspace/IFCO_Challenge
# MAGIC
# MAGIC # TESTS 05
# MAGIC export PYTHONPATH="/Workspace/IFCO_Challenge"
# MAGIC
# MAGIC PYTHONDONTWRITEBYTECODE=1 pytest tests/test_05.py -v -o cache_dir=/tmp/.pytest_cache