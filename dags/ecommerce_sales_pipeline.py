
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from scripts.extract import extract_sales
from scripts.validates import validate_sales
from scripts.transform import transform_sales


default_args = {
    'owner': 'Imad',
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}


def check_data_availability():
    import os

    if not os.path.exists("data/raw/sales.csv"):
        raise FileNotFoundError("sales.csv not found!")

    print("Sales data is available.")


with DAG(
    dag_id='ecommerce_sales_pipeline',
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
        op_args=["data/processed/extracted_sales.csv"]
    )

    task4 = PythonOperator(
        task_id='transform_sales',
        python_callable=transform_sales,
        op_args=["data/processed/extracted_sales.csv"]
    )

    task5 = PythonOperator(
        task_id='load_sales',
        python_callable=lambda: print("Loading sales into PostgreSQL")
    )

    task1 >> task2 >> task3 >> task4 >> task5
