# src/transformations.py
import re
import json
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def normalize_company_name(name):
    if not name:
        return ""
    name = name.lower()
    name = re.sub(r"[^a-z0-9 ]", "", name)
    return name.strip()


def get_crate_distribution_by_company(df: DataFrame) -> DataFrame:
    """
    Calculate the distribution of crate types per company
    """
    # 1. Definimos la ventana sobre la columna de agrupación
    window_company = Window.partitionBy("company_name_clean")

    return (
        df
        .filter(F.col("crate_type").isNotNull())
        # 2. First group
        .groupBy("company_name_clean", "crate_type")
        .agg(F.count("*").alias("num_orders"))
        # 3. Company's total
        .withColumn(
            "pct_crate_by_company",
            F.round(
                F.col("num_orders") * 100.0 / F.sum("num_orders").over(window_company),
                2
            )
        )
        .orderBy("company_name_clean", "crate_type")
    )


def get_full_name(raw: str) -> str:
    """
    Extracts full name from contact_data.
    'John Doe' is used if no info is available.
    """
    contact = parse_contact_json(raw)
    name    = (contact.get("contact_name")    or "").strip()
    surname = (contact.get("contact_surname") or "").strip()

    if name and surname:
        return f"{name} {surname}"
    if name:
        return name
    if surname:
        return surname
    return "John Doe"


def get_address(raw: str) -> str:
    """
    Extracts an address with the format: "city name, postal code". If the city name is not available, the placeholder "Unknown" should be used. If the postal code is not known, the placeholder "UNK00" should be used.
    """
    contact = parse_contact_json(raw)

    city = (contact.get("city") or "").strip()
    cp   = str(contact.get("cp") or "").strip()

    # Validamos que cp no sea un string vacío tras el cast
    if not city:
        city = "Unknown"
    if not cp:
        cp = "UNK00"

    return f"{city}, {cp}"


def calculate_net_value_eur(gross_cents: int, vat_pct: float) -> float:
    """
    Calculates the net value in euros from the gross value in cents and the VAT
    net = gross / (1 + vat/100) / 100
    """
    if gross_cents is None or vat_pct is None:
        return 0.0
    net = gross_cents / (1 + vat_pct / 100) / 100
    return round(net, 2)

def get_commission_rate(position: int) -> float:
    """
    Returns the commission rate based on the salesowner's position.
    Position 1 (main owner):  6%
    Position 2 (co-owner 1):  2.5%
    Position 3 (co-owner 2):  0.95%
    Other / Rest:             0%
    """
    rates = {1: 0.06, 2: 0.025, 3: 0.0095}
    return rates.get(position, 0.0)
