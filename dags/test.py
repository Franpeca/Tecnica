# ejemplo_simple_dag.py
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

# Definir el DAG
dag = DAG(
    'simple_dag',
    default_args={'start_date': days_ago(1)},
    description='Un DAG super simple',
    schedule_interval='@daily',  # Ejecuta el DAG todos los días
)

# Tarea
simple_task = DummyOperator(
    task_id='simple_task',
    dag=dag,
)