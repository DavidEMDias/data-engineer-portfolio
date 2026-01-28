import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
import random
import time

sys.path.append('/opt/airflow/api-request')

from insert_records import connect_to_db, insert_records, create_table
from api_request import fetch_data

#Cities to fetch weather data for
cities = ["Paris", "London", "Lisbon"]

#Function to fetch data and insert into DB
def fetch_and_insert(city):
    conn = connect_to_db()
    try:
        create_table(conn)
        data = fetch_data(city)
        insert_records(conn, data)
        print(f"Data for {city} inserted successfully.")
    finally:
        conn.close()

#Function to wait random time between 20 and 25 seconds and workaround API rate limits
def wait_random():
    wait_time = random.randint(20, 25)
    print(f"Waiting for {wait_time} seconds before next task...")
    time.sleep(wait_time)

default_args = {
    "description": "A DAG to orchestrate weather data ingestion for multiple cities",
    "start_date": datetime(2025, 12, 30),
    "catchup": False,
}

dag = DAG(
    dag_id='weather-api-multiple-cities-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=30)
)

with dag:
    previous_task = None

    for i, city in enumerate(cities):
        #Main task to fetch and insert data for each city
        city_task = PythonOperator(
            task_id=f'ingest_{city.lower()}',
            python_callable=lambda c=city: fetch_and_insert(c)
        )

        if previous_task:
            #Task to wait random time between city tasks
            wait_task = PythonOperator(
                task_id=f'wait_before_{city.lower()}',
                python_callable=wait_random
            )
            previous_task >> wait_task >> city_task #Setting dependencies between tasks for the first For loop iteration previous task and wait task do not exist (have value None)

        previous_task = city_task

    #Task to trigger the dbt DAG after all city tasks are done
    trigger_dbt_dag = TriggerDagRunOperator(
        task_id='trigger_dbt_dag',
        trigger_dag_id='weather-dbt-orchestrator',
        wait_for_completion=False
    )

    previous_task >> trigger_dbt_dag
