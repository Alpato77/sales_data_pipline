ARG AIRFLOW_BASE_IMAGE=apache/airflow:3.4.0
FROM ${AIRFLOW_BASE_IMAGE}

USER airflow
RUN pip install --no-cache-dir "pandas>=2.2,<3"
