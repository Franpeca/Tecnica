from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 9),
    'retries': 1,
}

# Función para vaciar la tabla
def truncate_table():
    pg_hook = PostgresHook(postgres_conn_id='postgres_data_conn')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    try:
        # Vaciar la tabla 'clean_data'
        cursor.execute("TRUNCATE TABLE clean_data RESTART IDENTITY CASCADE;")
        conn.commit()
        print("Tabla 'clean_data' vaciada correctamente.")
    
    except Exception as e:
        print(f"Error al vaciar la tabla 'clean_data': {str(e)}")
        raise

    finally:
        cursor.close()
        conn.close()

# Función para verificar si la tabla está vacía
def check_table_empty():
    pg_hook = PostgresHook(postgres_conn_id='postgres_data_conn')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    try:
        # Verificar si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM clean_data;")
        row_count = cursor.fetchone()[0]
        
        if row_count > 0:
            raise Exception(f"La tabla 'clean_data' no está vacía, tiene {row_count} registros.")
        else:
            print("La tabla 'clean_data' está vacía.")
    
    except Exception as e:
        print(f"Error al verificar si la tabla está vacía: {str(e)}")
        raise

    finally:
        cursor.close()
        conn.close()

with DAG(
    '04_truncate_clean_data_table',  # Nombre del DAG
    default_args=default_args,
    schedule_interval=None,  # Solo ejecución manual
    catchup=False
) as dag:

    # Tarea 1: Vaciar la tabla 'clean_data'
    truncate_table_task = PythonOperator(
        task_id="truncate_table",
        python_callable=truncate_table,
        retries=0
    )

    # Tarea 2: Verificar si la tabla 'clean_data' está vacía
    check_table_empty_task = PythonOperator(
        task_id="check_table_empty",
        python_callable=check_table_empty,
        retries=0
    )

    # Asignamos el orden de las tareas
    truncate_table_task >> check_table_empty_task
