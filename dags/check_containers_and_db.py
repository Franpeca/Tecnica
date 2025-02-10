from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSkipException
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import docker
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 9),
    'retries': 1,
}

# Función para verificar si el contenedor de Kedro está corriendo
def check_kedro_container():
    client = docker.from_env()
    container_name = "kedro_container"
    containers = client.containers.list(filters={"name": container_name})
    
    if not containers:
        raise Exception(f"El contenedor {container_name} no está corriendo. Lánzalo con Docker Compose.")

# Función para verificar si el contenedor de PostgreSQL está corriendo
def check_postgres_container():
    client = docker.from_env()
    container_name = "postgres_db"  # Cambia esto por el nombre de tu contenedor PostgreSQL
    containers = client.containers.list(filters={"name": container_name})
    
    if not containers:
        raise Exception(f"El contenedor {container_name} no está corriendo. Lánzalo con Docker Compose")

# Función para verificar si la base de datos 'data_db' existe en PostgreSQL
def check_data_db_exists():
    hook = PostgresHook(postgres_conn_id='postgres_data_conn')  # Asegúrate de que el ID de la conexión sea correcto
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Ejecutar consulta para verificar si la base de datos 'data_db' existe
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'data_db';")
    exists = cursor.fetchone()

    if exists:
        print("La base de datos 'data_db' existe.")
    else:
        raise Exception("La base de datos 'data_db' NO existe.")

    cursor.close()
    conn.close()

with DAG(
    '01_check_containers_and_db',  # Nombre del DAG
    default_args=default_args,
    schedule_interval=None,  # Solo ejecución manual
    catchup=False
) as dag:

    # Tarea 1: Verificar si el contenedor Kedro está corriendo
    check_container = PythonOperator(
        task_id="check_kedro_container",
        python_callable=check_kedro_container,
        retries=0,  # Evita reintentos
    )

    # Tarea 2: Verificar si el contenedor PostgreSQL está corriendo
    check_postgres = PythonOperator(
        task_id="check_postgres_container",
        python_callable=check_postgres_container,
        retries=0,  # Evita reintentos
    )

    # Tarea 3: Verificar si la base de datos 'data_db' existe en PostgreSQL
    check_data_db = PythonOperator(
        task_id="check_data_db_exists",
        python_callable=check_data_db_exists,
        retries=0,  # Evita reintentos
    )

    # Ejecutar las tareas en orden
    check_container >> check_postgres >> check_data_db
