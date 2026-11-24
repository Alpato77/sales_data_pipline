
def validate_sales(df):

    # Check missing customer IDs
    if df["customer_id"].isnull().any():
        print("WARNING: Missing customer_id values detected!")

    # Check duplicate order IDs
    if df["order_id"].duplicated().any():
        print("WARNING: Duplicate order_id values detected!")

    # Check negative quantities
    if (df["quantity"] < 0).any():
        print("WARNING: Negative quantities detected!")

    print("Validation completed.")

    return df
