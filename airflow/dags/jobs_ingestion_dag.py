import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.jobs_pipeline.db import insert_raw_jobs

with DAG(
    dag_id="jobs_raw_ingestion",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["jobs", "raw", "postgres"],
) as dag:

    ingest_raw_jobs = PythonOperator(
        task_id="insert_raw_jobs",
        python_callable=insert_raw_jobs,
    )
