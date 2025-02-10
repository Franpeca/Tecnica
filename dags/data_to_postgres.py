from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSkipException
from datetime import datetime
import docker

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 9),
    'retries': 1,
}

def check_dataset_exists():
    container_name = "kedro_container"
    dataset_path = "/home/kedro_docker/kedro_project/data/01_raw/clean_data.csv"  # Ruta dentro del contenedor
    
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        
        # Ejecutar el comando test -f para verificar si el archivo existe en el volumen del contenedor
        exit_code, _ = container.exec_run(f"test -f {dataset_path}")
        
        # Si el exit_code no es 0, el archivo no existe
        if exit_code != 0:
            raise Exception(f"El dataset no existe en la ruta {dataset_path}.")
    
    except docker.errors.NotFound:
        raise Exception(f"Contenedor {container_name} no encontrado.")
    except Exception as e:
        raise Exception(f"Error al comprobar el dataset: {str(e)}")

# Función para manejar el fallo de la tarea específica
def handle_check_dataset_failure(context):
    print(f"Tarea {context['task_instance'].task_id} falló, pero se manejará de manera personalizada.")
    # Detener el DAG si no existe el dataset
    raise AirflowSkipException(f"Tarea {context['task_instance'].task_id} se saltó debido al fallo.")

with DAG(
    '03_data_to_postgres',  # Nombre del DAG
    default_args=default_args,
    schedule_interval=None,  # Solo ejecución manual
    catchup=False
) as dag:

    # Tarea 1: Verificar si el dataset existe dentro del contenedor de Kedro
    check_dataset = PythonOperator(
        task_id="check_dataset_exists",
        python_callable=check_dataset_exists,
        retries=0,  # Evita reintentos
        on_failure_callback=handle_check_dataset_failure  # Solo esta tarea tendrá un manejo personalizado de fallos
    )

    # Ejecutar la tarea
    check_dataset
