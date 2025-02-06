import uuid
import random
import pandas as pd
from faker import Faker
from datetime import datetime

def generate_data():
    print("\n\n----------------------------------------------------------------------")
    fake = Faker()
    data = []
    total_records = 0  # Contador para los registros generados
    null_target = int(5000 * 0.02)  # 2% de 5000 (100 registros)
    typo_target = int(5000 * 0.02)  # Otro 2% de 5000 (100 registros)
    null_count = 0
    typo_count = 0

    while total_records < 5000:
        id = str(uuid.uuid4())
        name = fake.name()
        email = fake.email()
        age = random.randint(18, 80)
        signup_date = fake.date_this_decade().strftime("%Y-%m-%d")

        # Introducir errores de forma aleatoria sin agruparlos
        if random.random() < 0.02 and null_count < null_target:  # 2% de nulos
            if random.random() < 1/3:
                name = None
            if random.random() < 1/3:
                email = None
            if random.random() < 1/3:
                signup_date = None
            null_count += 1

        if random.random() < 0.02 and typo_count < typo_target:  # 2% de errores tipográficos
            if random.random() < 0.5 and name:  # Evitar errores en None
                pos = random.randint(0, len(name) - 1)
                name = name[:pos] + random.choice("abcdefghijklmnopqrstuvwxyz") + name[pos + 1:]
            else:
                if email:  # Evitar errores en None
                    pos = random.randint(0, len(email) - 1)
                    email = email[:pos] + random.choice("abcdefghijklmnopqrstuvwxyz") + email[pos + 1:]
            typo_count += 1

        # Introducir duplicados (10%)
        if random.random() < 0.1 and data:
            data.append(data[random.randint(0, len(data)-1)])
            total_records += 1  # Contamos el duplicado como un registro válido

        # Añadir un nuevo registro
        data.append([id, name, email, age, signup_date])
        total_records += 1

    df = pd.DataFrame(data, columns=["id", "name", "email", "age", "signup_date"])
    
    # Guardar en CSV
    df.to_csv('messy_data.csv', index=False)
    print("\n\n\n")
    print(df)
    df.describe()
    print("\n\n\n")
    print("Datos generados y guardados en 'messy_data.csv'")
    return "datos_generados"

if __name__ == "__main__":
    generate_data()
