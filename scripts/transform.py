import pandas as pd

def transform_sales(df):

    # Remove duplicate orders
    df = df.drop_duplicates(subset=["order_id"])

    # Remove rows with missing customer_id
    df = df.dropna(subset=["customer_id"])

    # Remove rows with negative quantities
    df = df[df["quantity"] >= 0]

    # Calculate total amount for each order
    df["total_amount"] = df["quantity"] * df["unit_price"]

    # Convert order_date to datetime
    df["order_date"] = pd.to_datetime(df["order_date"])

    print(f"Transformation completed: {len(df)} rows remaining.")

    return df
