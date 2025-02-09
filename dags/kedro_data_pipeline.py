from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

# Definir el DAG
dag = DAG(
    'kedro_data_pipeline',
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    schedule_interval=None,
    start_date=datetime(2025, 2, 8),
)

# Definir el DockerOperator para ejecutar Kedro dentro del contenedor
run_kedro = DockerOperator(
    task_id='run_kedro',
    image='kedro_img',  # La imagen de Kedro ya debe estar levantada
    container_name='kedro_container',  # Asegúrate de que este nombre coincida con el del contenedor levantado
    command='cd /home/kedro_docker/kedro_project && kedro run',  # Ejecutar el comando kedro run
    docker_url='unix://var/run/docker.sock',  # Esto es estándar, si tienes Docker corriendo localmente
    network_mode='bridge',  # O usa el modo de red adecuado para tu contenedor
    dag=dag,
)
