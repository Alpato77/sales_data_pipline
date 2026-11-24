import pandas as pd
def validate_sales(df):

    # Check missing values
    if df["customer_id"].isnull().any():
        raise ValueError("Missing customer_id values detected!")

    # Check duplicate order IDs
    if df["order_id"].duplicated().any():
        raise ValueError("Duplicate order_id values detected!")

    # Check negative quantities
    if (df["quantity"] < 0).any():
        raise ValueError("Negative quantities detected!")

    print("Data validation successful!")

    return df
