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

# Función para verificar si el dataset existe dentro del contenedor de Kedro
def check_dataset_exists():
    container_name = "kedro_container"
    dataset_path = "/home/kedro_docker/kedro_project/data/01_raw/clean_data.csv"
    
    client = docker.from_env()
    container = client.containers.get(container_name)
    
    # Ejecutamos el comando test -f para verificar si el archivo existe
    exit_code, _ = container.exec_run(f"test -f {dataset_path}")
    
    # Si el exit_code no es 0, el archivo no existe
    if exit_code != 0:
        raise Exception(f"El dataset no existe en la ruta {dataset_path}.")

# Función para verificar si la base de datos 'dataset_db' existe en PostgreSQL
def check_postgres_db_exists():
    hook = PostgresHook(postgres_conn_id='postgres_default')  # Asegúrate de que el ID de la conexión sea correcto
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Ejecutar consulta para verificar si la base de datos 'dataset_db' existe
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'dataset_db';")
    exists = cursor.fetchone()

    if exists:
        print("La base de datos 'dataset_db' existe.")
    else:
        raise Exception("La base de datos 'dataset_db' NO existe.")

    cursor.close()
    conn.close()

# Función para manejar el fallo de la tarea específica
def handle_check_dataset_failure(context):
    print(f"Tarea {context['task_instance'].task_id} falló, pero se manejará de manera personalizada.")
    # Aquí puedes agregar lógica personalizada para manejar el fallo
    # Si no quieres que falle el DAG, podrías incluso saltar la tarea (opcional)
    raise AirflowSkipException(f"Tarea {context['task_instance'].task_id} se saltó debido al fallo!.")

with DAG(
    'data_to_postgres',  # Nombre del DAG
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

    # Tarea 3: Verificar si el dataset existe dentro del contenedor de Kedro
    check_dataset = PythonOperator(
        task_id="check_dataset_exists",
        python_callable=check_dataset_exists,
        retries=0,  # Evita reintentos
        on_failure_callback=handle_check_dataset_failure  # Solo esta tarea tendrá un manejo personalizado de fallos
    )

    # Tarea 4: Verificar si la base de datos 'dataset_db' existe en PostgreSQL
    check_postgres_db = PythonOperator(
        task_id="check_postgres_db_exists",
        python_callable=check_postgres_db_exists,
        retries=0,  # Evita reintentos
    )

    # Ejecutar las tareas en orden
    check_container >> check_postgres >> check_dataset >> check_postgres_db
