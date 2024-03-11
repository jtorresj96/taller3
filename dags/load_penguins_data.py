from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
from sqlalchemy import create_engine

def load_data():
    # Configura la conexión a la base de datos
    engine = create_engine('mysql+mysqlconnector://user:password@mysql/airflow_workshop')
    df = pd.read_csv('/opt/airflow/data/penguins_size.csv')
    df.to_sql('penguins', con=engine, if_exists='replace', index=False)

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    'load_penguins_data',
    default_args=default_args,
    description='Load penguins data into MySQL DB',
    schedule_interval=None,
) as dag:

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    load_task
