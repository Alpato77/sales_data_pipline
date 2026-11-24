
import pandas as pd


def transform_sales(file_path):

    df = pd.read_csv(file_path)

    df = df.drop_duplicates(subset=["order_id"])
    df = df.dropna(subset=["customer_id"])
    df = df[df["quantity"] >= 0]

    df["total_amount"] = df["quantity"] * df["unit_price"]

    df["order_date"] = pd.to_datetime(df["order_date"])

    df.to_csv("data/processed/transformed_sales.csv", index=False)

    print(f"Transformation completed: {len(df)} rows.")

    return "data/processed/transformed_sales.csv"
