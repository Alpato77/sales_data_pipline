

import pandas as pd


REQUIRED_COLUMNS = {"order_id", "customer_id", "product_id", "quantity", "unit_price", "order_date"}


def validate_sales(file_path):

    df = pd.read_csv(file_path)
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")

    if df.empty:
        raise ValueError("Sales file contains no rows")

    if df["customer_id"].isnull().any():
        print("WARNING: Missing customer_id detected!")

    if df["order_id"].duplicated().any():
        print("WARNING: Duplicate order_id detected!")

    if (pd.to_numeric(df["quantity"], errors="coerce") < 0).any():
        print("WARNING: Negative quantities detected!")

    if (pd.to_numeric(df["unit_price"], errors="coerce") < 0).any():
        print("WARNING: Negative unit prices detected!")

    print("Validation completed.")

    return file_path
