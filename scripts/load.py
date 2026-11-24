import csv
from pathlib import Path

from airflow.providers.postgres.hooks.postgres import PostgresHook


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRANSFORMED_FILE = PROJECT_ROOT / "data" / "processed" / "transformed_sales.csv"


def load_sales(file_path=str(TRANSFORMED_FILE)):
    """Load transformed sales into PostgreSQL, updating orders already loaded."""
    input_file = Path(file_path)
    if not input_file.is_file():
        raise FileNotFoundError(f"Transformed sales file not found: {input_file}")

    insert_sql = """
        INSERT INTO sales (
            order_id, customer_id, product_id, quantity, unit_price,
            order_date, status, total_amount
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO UPDATE SET
            customer_id = EXCLUDED.customer_id,
            product_id = EXCLUDED.product_id,
            quantity = EXCLUDED.quantity,
            unit_price = EXCLUDED.unit_price,
            order_date = EXCLUDED.order_date,
            status = EXCLUDED.status,
            total_amount = EXCLUDED.total_amount
    """

    with input_file.open("r", newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    values = [
        (
            int(float(row["order_id"])),
            int(float(row["customer_id"])),
            int(float(row["product_id"])),
            int(row["quantity"]),
            row["unit_price"],
            row["order_date"],
            row.get("status") or None,
            row["total_amount"],
        )
        for row in rows
    ]

    hook = PostgresHook(postgres_conn_id="sales_postgres")
    with hook.get_conn() as connection:
        with connection.cursor() as cursor:
            cursor.executemany(insert_sql, values)

    print(f"Loaded {len(values)} sales rows into PostgreSQL.")
    return len(values)
