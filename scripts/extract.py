

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "sales.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def extract_sales():

    if not RAW_FILE.is_file():
        raise FileNotFoundError(f"Sales input file not found: {RAW_FILE}")

    df = pd.read_csv(RAW_FILE)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_file = PROCESSED_DIR / "extracted_sales.csv"
    df.to_csv(output_file, index=False)

    print(f"Extracted {len(df)} rows.")

    return str(output_file)
