import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta

sys.path.append('/opt/airflow/api-request')

def safe_main_callable():
    from insert_records import main
    return main()


default_args = {
    "description": "A DAG to orchestrate data",
    "start_date": datetime(2025, 12, 30),
    "catchup":False, #backfill with previous runs
}

dag = DAG(
    dag_id = 'weather-api-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=30)
)

with dag:

    ingest_task  = PythonOperator(
        task_id = 'ingest_data_task',
        python_callable = safe_main_callable
    )

    # Task to trigger DAG 2
    trigger_dbt_dag = TriggerDagRunOperator(
        task_id='trigger_dbt_dag',
        trigger_dag_id='weather-dbt-orchestrator',  # DAG 2
        wait_for_completion=False  # doesn't wait for dag 2 to finish
    )


     # Ordem de execução
    ingest_task >> trigger_dbt_dag