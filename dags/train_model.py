
from airflow.sensors.external_task import ExternalTaskSensor
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

def train_penguin_sex_model():
    # Configura la conexión a la base de datos
    engine = create_engine('mysql+mysqlconnector://user:password@mysql/airflow_workshop')

    # Carga los datos de la base de datos
    df = pd.read_sql_table('penguins', engine)
    
    # Elimina filas con valores faltantes
    df = df.dropna(subset=['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex'])
    
    df = df[df['sex'].isin(['MALE', 'FEMALE'])]

    # Conversión de categorías a números
    df['sex'] = df['sex'].map({'MALE': 0, 'FEMALE': 1})

    # Define las características y la etiqueta
    X = df[['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g']]
    y = df['sex']

    # Divide los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrena el modelo de regresión logística
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    # Predicciones y evaluación del modelo
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f'Accuracy: {accuracy}')

    # Guarda el modelo entrenado
    with open('/opt/airflow/data/model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # Para usar este dato en otras tareas, lo pasamos usando xcom
    # ti.xcom_push(key='model_accuracy', value=accuracy)

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'catchup': False,
}

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'train_penguin_sex_model',
    default_args=default_args,
    description='Train a logistic regression model on penguins data',
    schedule_interval=None,
    catchup=False,
) as dag:

    train_model = PythonOperator(
        task_id='train_model',
        python_callable=train_penguin_sex_model,
    )

    train_model