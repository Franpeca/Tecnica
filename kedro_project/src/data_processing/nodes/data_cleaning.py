import pandas as pd
import re
from datetime import datetime

def clean_data(messy_data):
    print("\n\n|||||| Nodo de limpieza de datos ||||||")

    print("|> -- Limpiando datos...")

    # Creamos una copia de messy_data para no modificar el dataset original
    # Kedro pasa los datos por referencia
    df = messy_data.copy()
    
    # 1. Eliminar duplicados basados en la columna 'id'
    df = df.drop_duplicates(subset="id", keep="first")
    
    # 2. Gestión de valores nulos:
    # Reemplazar valores nulos en 'name' con 'Unknown'
    df['name'] = df['name'].fillna('Unknown')

    # Reemplazar valores nulos en 'email' con 'unknown@example.com'
    df['email'] = df['email'].fillna('unknown@example.com')

    # Reemplazar valores nulos en 'signup_date' con la fecha más frecuente (o fecha actual)
    most_frequent_date = df['signup_date'].mode()[0] if not df['signup_date'].isnull().all() else str(datetime.now().date())
    df['signup_date'] = df['signup_date'].fillna(most_frequent_date)
    
    # 3. Corrección de errores tipográficos:
    # Corregir el campo 'email' utilizando expresión regular
    df['email'] = df['email'].apply(
        lambda email: email if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zAZ0-9.-]+\.[a-zA-Z]{2,}$', email) else 'unknown@example.com'
    )
    
    # Limpiar el campo 'name' eliminando caracteres no deseados
    df['name'] = df['name'].apply(
        lambda name: re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s\.\-]', '', name)
    )

    # 4. Validación de fechas:
    # Convertir el campo 'signup_date' a un formato de fecha (datetime)
    df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')

    # Si la conversión falla, asignamos la fecha actual
    df['signup_date'] = df['signup_date'].fillna(datetime.now())

    # Mostrar el DataFrame limpio para verificar
    print("\n\n|> -- Resultados de los datos limpios:\n")

    df.info()

    print("\n\n|> -- Datos limpiados y guardados en 'clean_data.csv'")
    print("|||||||||||||||||||||||||||||||||||||||||||\n\n")

    # El data catalog lo guardará con el nombre correcto
    return df
