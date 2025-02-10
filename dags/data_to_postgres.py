from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.exceptions import AirflowSkipException
from datetime import datetime
import docker
import csv

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 9),
    'retries': 1,
}

# Comprobacion de la existencia del dataset generado por Kedro
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

# Función para manejar el fallo de la tarea especifica para el caso de que no exista el dataset
def handle_check_dataset_failure(context):
    print(f"Tarea {context['task_instance'].task_id} falló, pero se manejará de manera personalizada.")
    # Detener el DAG si no existe el dataset
    raise AirflowSkipException(f"Tarea {context['task_instance'].task_id} se saltó debido al fallo.")

# Comprobacion de la existencia de la tabla, si no existe, se crea
def check_and_create_table():
    pg_hook = PostgresHook(postgres_conn_id='postgres_data_conn')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    # Verificar si la tabla existe
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'clean_data')")
    exists = cursor.fetchone()[0]
    
    if not exists:
        try:
            # Intentar crear la tabla si no existe
            cursor.execute("""
                CREATE TABLE clean_data (
                    id UUID PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100),
                    age INT,
                    signup_date DATE
                );
            """)
            conn.commit()
            print("Tabla 'clean_data' creada.")
        except Exception as e:
            print(f"Error al crear la tabla 'clean_data': {str(e)}")
            raise Exception("No se pudo crear la tabla 'clean_data'.")
    else:
        print("La tabla 'clean_data' ya existe.")

    cursor.close()
    conn.close()

# Funcion para manejar el fallo de la tarea especifica (para la creacion de la tabla)
def handle_check_and_create_failure(context):
    print(f"Tarea {context['task_instance'].task_id} falló, pero se manejará de manera personalizada.")
    raise AirflowSkipException(f"Tarea {context['task_instance'].task_id} se saltó debido al fallo.")

# Función para insertar los datos del CSV en la tabla clean_data
def insert_data_to_db():
    dataset_path = "/home/kedro_docker/kedro_project/data/01_raw/clean_data.csv"  # Ruta del CSV en el contenedor
    
    try:
        client = docker.from_env()
        container = client.containers.get("kedro_container")

        # Leer el archivo CSV desde el contenedor
        exit_code, output = container.exec_run(f"cat {dataset_path}")
        
        if exit_code != 0:
            handle_insert_data_error(f"No se pudo leer el archivo {dataset_path}.")
        
        # Convertimos el contenido en texto a una lista de registros
        data = output.decode("utf-8").splitlines()
        
        # Usamos el primer registro como cabecera
        reader = csv.DictReader(data)
        
        pg_hook = PostgresHook(postgres_conn_id='postgres_data_conn')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        
        for row in reader:
            print(f"Inserting row: {row}")  # Añadir log de cada fila
            cursor.execute("""
                INSERT INTO clean_data (id, name, email, age, signup_date)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (row['id'], row['name'], row['email'], row['age'], row['signup_date']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Datos insertados correctamente en la tabla 'clean_data'.")
    
    except Exception as e:
        handle_insert_data_error(f"Error al insertar los datos: {str(e)}")

# Función para manejar errores en la tarea de inserción de datos
def handle_insert_data_error(error_message):
    """
    Función para manejar los errores específicos de la tarea de inserción de datos,
    logueando el error y lanzando una excepción clara.
    """
    print(f"Error: {error_message}")
    raise AirflowSkipException(f"Error: {error_message}")

with DAG(
    '03_data_to_postgres',  # Nombre del DAG
    default_args=default_args,
    schedule_interval=None,  # Solo ejecucion manual
    catchup=False
) as dag:

    # Tarea 1: Verificar si el dataset existe dentro del contenedor de Kedro
    check_dataset = PythonOperator(
        task_id="check_dataset_exists",
        python_callable=check_dataset_exists,
        retries=0,  # Evita reintentos
        on_failure_callback=handle_check_dataset_failure  # Solo esta tarea tendra un manejo personalizado de fallos
    )

    # Tarea 2: Verificar si la tabla 'clean_data' existe y crearla si no existe
    check_and_create_table_task = PythonOperator(
        task_id="check_and_create_table",
        python_callable=check_and_create_table,
        retries=0,
        on_failure_callback=handle_check_and_create_failure
    )

    # Tarea 3: Insertar los datos en la base de datos
    insert_data = PythonOperator(
        task_id="insert_data_to_db",
        python_callable=insert_data_to_db,
        retries=0,
        on_failure_callback=handle_insert_data_error  # Agregado para manejar fallos de forma centralizada
    )

    # Asignamos las tareas de ejecución en orden
    check_dataset >> check_and_create_table_task >> insert_data
