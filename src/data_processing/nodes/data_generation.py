import uuid
import random
import pandas as pd
from faker import Faker


def generate_data():
    print("\n\n|||||| Nodo de generación de datos ||||||")
    print("|> -- Generando datos...")
    
    
    fake = Faker()
    data = []

    total_records = 5000  # Definimos la cantidad total de registros
    num_nulls = int(total_records * 0.02)  # Aquí aplicamos un 2% de valores nulos en name, email y signup_date
    num_typos = int(total_records * 0.02)  # Aquí aplicamos un 2% de errores tipográficos en name y email
    num_duplicates = int(total_records * 0.10)  # Aquí aplicamos un 10% de registros duplicados

    # Aquí generamos los registros iniciales, sin contar los duplicados aún
    for _ in range(total_records - num_duplicates):  
        id = str(uuid.uuid4())  # Generamos un UUID único
        name = fake.name()  # Generamos un nombre aleatorio
        email = fake.email()  # Generamos un email aleatorio
        age = random.randint(18, 80)  # Generamos una edad aleatoria entre 18 y 80
        signup_date = fake.date_this_decade().strftime("%Y-%m-%d")  # Generamos una fecha de registro

        data.append([id, name, email, age, signup_date])  # Añadimos el registro a la lista de datos

    # Aquí creamos un DataFrame con los datos generados
    df = pd.DataFrame(data, columns=["id", "name", "email", "age", "signup_date"])

    # Aquí seleccionamos índices aleatorios para introducir valores nulos en las tres columnas
    null_indices = random.sample(range(len(df)), num_nulls * 3)  # Seleccionamos 3 veces el número de nulos
    for i in range(num_nulls):
        df.at[null_indices[i], "name"] = None  # Hacemos nulo el campo name
        df.at[null_indices[i + num_nulls], "email"] = None  # Hacemos nulo el campo email
        df.at[null_indices[i + (num_nulls * 2)], "signup_date"] = None  # Hacemos nulo el campo signup_date

    # Aquí aplicamos errores tipográficos, asegurándonos de que no afecten valores nulos
    typo_indices = random.sample([i for i in range(len(df)) if i not in null_indices], num_typos * 2)
    for i in range(num_typos):
        df.at[typo_indices[i], "name"] = df.at[typo_indices[i], "name"][:-1] + random.choice("xyz") if df.at[typo_indices[i], "name"] else None
        # Introducimos un error tipográfico en name reemplazando el último carácter por una letra aleatoria
        
        df.at[typo_indices[i + num_typos], "email"] = df.at[typo_indices[i + num_typos], "email"].replace("@", str(random.randint(0, 9)) + "@") if df.at[typo_indices[i + num_typos], "email"] else None
        # Introducimos un error tipográfico en email, reemplazando el "@" por un número aleatorio y luego "@"

    # Aquí generamos los duplicados eligiendo registros aleatorios
    duplicate_indices = random.choices(range(len(df)), k=num_duplicates)  # Seleccionamos registros aleatorios para duplicar
    duplicates = df.iloc[duplicate_indices]  # Extraemos los duplicados del DataFrame original
    df = pd.concat([df, duplicates], ignore_index=True)  # Añadimos los duplicados al DataFrame final

    print("\n\n|> -- Resultados de los datos generados:\n")

    df.info()

    print("\n\n|> -- Datos generados y guardados en 'messy_data.csv'")
    print("|||||||||||||||||||||||||||||||||||||||||||||\n\n")



    return df
