from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from simple_script import run


with DAG(
    dag_id="simple_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    PythonOperator(
        task_id="run_script",
        python_callable=run,
    )
