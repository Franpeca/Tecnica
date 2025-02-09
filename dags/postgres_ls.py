from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 9),
}

with DAG(
    'postgres_ls',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    list_postgres_files = DockerOperator(
        task_id='list_postgres_files',
        image='postgres:13',  # Imagen de PostgreSQL
        command='ls /var/lib/postgresql/data',  # Comando para listar los archivos
        auto_remove=True,  # Eliminar el contenedor después de la ejecución
        docker_url='unix://var/run/docker.sock',  # URL de Docker para conectarse al socket
        network_mode='bridge',  # Asegúrate de que los contenedores estén en la misma red
    )

    list_postgres_files
