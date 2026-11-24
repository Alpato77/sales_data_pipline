
import pandas as pd


def extract_sales():

    # Extract sales data from CSV
    df = pd.read_csv("data/raw/sales.csv")

    print(f"Successfully extracted {len(df)} rows.")

    return df
