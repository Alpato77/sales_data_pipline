
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# Default arguments
default_args = {
    'owner': 'Imad',
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}


# Task functions
def check_data_availability():
    print("Checking sales data availability")


def extract_sales():
    print("Extracting sales data")


def validate_sales():
    print("Validating sales data")


def transform_sales():
    print("Transforming sales data")


def load_sales():
    print("Loading sales into PostgreSQL")


# DAG definition
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
        python_callable=validate_sales
    )

    task4 = PythonOperator(
        task_id='transform_sales',
        python_callable=transform_sales
    )

    task5 = PythonOperator(
        task_id='load_sales',
        python_callable=load_sales
    )

    # Task dependencies
    task1 >> task2 >> task3 >> task4 >> task5
