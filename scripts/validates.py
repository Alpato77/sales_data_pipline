

import pandas as pd


def validate_sales(file_path):

    df = pd.read_csv(file_path)

    if df["customer_id"].isnull().any():
        print("WARNING: Missing customer_id detected!")

    if df["order_id"].duplicated().any():
        print("WARNING: Duplicate order_id detected!")

    if (df["quantity"] < 0).any():
        print("WARNING: Negative quantities detected!")

    print("Validation completed.")

    return file_path
