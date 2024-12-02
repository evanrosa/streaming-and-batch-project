from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

# Define default args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 1),
    'email_on_failure': False,
    'retries': 3,  # Increasing retries to handle transient errors
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
with DAG(
    'soccer_batch_processing',
    default_args=default_args,
    description='DAG for batch processing soccer data with Spark and loading to BigQuery',
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Step 1: Run Spark Job to transform data
    run_spark_job = BashOperator(
        task_id='run_spark_job',
        bash_command='spark-submit --master yarn /src/batch/spark_etl.py'
    )

    # Step 2: Load transformed data from GCS to BigQuery managed table
    load_to_bigquery_managed = BigQueryInsertJobOperator(
        task_id='load_to_bigquery_managed',
        configuration={
            "load": {
                "destinationTable": {
                    "projectId": 'optimaflo-sport',
                    "datasetId": 'soccer_data',
                    "tableId": 'soccer_matches'
                },
                "sourceUris": ["gs://soccer_data_bucket/transformed_data/soccer_matches/*.parquet"],
                "sourceFormat": "PARQUET",
                "writeDisposition": "WRITE_TRUNCATE",
                "autodetect": True
            }
        }
    )

    run_spark_job >> load_to_bigquery_managed
