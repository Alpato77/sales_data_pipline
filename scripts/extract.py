

import pandas as pd


def extract_sales():

    df = pd.read_csv("data/raw/sales.csv")

    df.to_csv("data/processed/extracted_sales.csv", index=False)

    print(f"Extracted {len(df)} rows.")

    return "data/processed/extracted_sales.csv"
