from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import docker
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 9),
    'retries': 1,
}

# Función para ejecutar el pipeline de Kedro dentro del contenedor
def run_kedro_pipeline():
    try:
        client = docker.from_env()
        container_name = "kedro_container"
        container = client.containers.get(container_name)
        
        # Ejecutar el comando dentro del contenedor
        command = "bash -c 'cd kedro_project && kedro run'"
        result = container.exec_run(command, tty=True, stdout=True, stderr=True)
        
        # Mostrar los logs de la ejecución del comando
        output = result.output.decode()
        print(output)
        
        # Verificar si hubo un error
        if "ERROR" in output:
            raise Exception("Hubo un error durante la ejecución del pipeline Kedro!.")
        
    except Exception as e:
        # Manejo de errores
        print(f"Error al ejecutar el pipeline de Kedro: {str(e)}")
        raise

with DAG(
    '02_kedro_run',
    default_args=default_args,
    schedule_interval=None,  # Solo ejecución manual
    catchup=False
) as dag:

    run_kedro = PythonOperator(
        task_id='run_kedro_pipeline',
        python_callable=run_kedro_pipeline
    )

    run_kedro  # Asegura que primero se verifique el contenedor antes de ejecutar Kedro
