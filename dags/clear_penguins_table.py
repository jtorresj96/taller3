from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine

def clear_data():
    engine = create_engine('mysql+mysqlconnector://user:password@mysql/airflow_workshop')
    with engine.connect() as conn:
        conn.execute("TRUNCATE TABLE penguins;")

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    'clear_penguins_table',
    default_args=default_args,
    description='Clear penguins table in MySQL DB',
    schedule_interval=None,
) as dag:

    clear_task = PythonOperator(
        task_id='clear_data',
        python_callable=clear_data,
    )

    clear_task
