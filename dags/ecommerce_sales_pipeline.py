
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pathlib import Path

from scripts.extract import extract_sales
from scripts.validates import validate_sales
from scripts.transform import transform_sales


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXTRACTED_FILE = str(PROJECT_ROOT / "data" / "processed" / "extracted_sales.csv")


default_args = {
    'owner': 'Imad',
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}


def check_data_availability():
    sales_file = PROJECT_ROOT / "data" / "raw" / "sales.csv"
    if not sales_file.is_file():
        raise FileNotFoundError(f"sales.csv not found: {sales_file}")

    print("Sales data is available.")


with DAG(
    dag_id='hello_myfirst_pipline',
    default_args=default_args,
    description='E-commerce Sales ETL Pipeline',
    start_date=datetime(2026, 11, 24),
    schedule='@daily',
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='check_data_availability',
        python_callable=check_data_availability
    )

    task2 = PythonOperator(
        task_id='extract_sales',
        python_callable=extract_sales
    )

    task3 = PythonOperator(
        task_id='validate_sales',
        python_callable=validate_sales,
        op_args=[EXTRACTED_FILE]
    )

    task4 = PythonOperator(
        task_id='transform_sales',
        python_callable=transform_sales,
        op_args=[EXTRACTED_FILE]
    )

    task5 = PythonOperator(
        task_id='load_sales',
        python_callable=lambda: print("Loading sales into PostgreSQL")
    )

    task1 >> task2 >> task3 >> task4 >> task5
