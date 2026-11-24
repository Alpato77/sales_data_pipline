
from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"


def transform_sales(file_path):

    df = pd.read_csv(file_path)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.drop_duplicates(subset=["order_id"])
    df = df.dropna(subset=["customer_id"])
    df = df.dropna(subset=["quantity", "unit_price", "order_date"])
    df = df[(df["quantity"] >= 0) & (df["unit_price"] >= 0)]

    df["total_amount"] = df["quantity"] * df["unit_price"]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_file = PROCESSED_DIR / "transformed_sales.csv"
    df.to_csv(output_file, index=False)

    print(f"Transformation completed: {len(df)} rows.")

    return str(output_file)
