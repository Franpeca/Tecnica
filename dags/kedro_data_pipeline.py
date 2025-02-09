from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import docker

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 9),
    'retries': 1,
}

# Función para verificar si el contenedor está corriendo
def check_kedro_container():
    client = docker.from_env()
    container_name = "kedro_container"
    containers = client.containers.list(filters={"name": container_name})
    
    if not containers:
        raise Exception(f"El contenedor {container_name} no está corriendo. Lánzalo con Docker Compose.")

with DAG(
    'kedro_run_dag',
    default_args=default_args,
    schedule_interval=None,  # Solo ejecución manual
    catchup=False
) as dag:

    check_container = PythonOperator(
        task_id="check_kedro_container",
        python_callable=check_kedro_container
    )

    # Usar BashOperator para ejecutar el comando dentro del contenedor
    run_kedro = BashOperator(
        task_id='run_kedro_pipeline',
        bash_command='docker exec kedro_container bash -c "cd kedro_project && kedro run"'
    )

    check_container >> run_kedro  # Asegura que primero se verifique el contenedor antes de ejecutar Kedro
