import uuid
import random
import pandas as pd
from faker import Faker
from datetime import datetime

def generate_data():
    print("\n\n----------------------------------------------------------------------")
    fake = Faker()
    data = []
    
    for _ in range(5000):
        id = str(uuid.uuid4())
        name = fake.name()
        email = fake.email()
        age = random.randint(18, 80)
        signup_date = fake.date_this_decade().strftime("%Y-%m-%d")
        
        # Introducir errores
        if random.random() < 0.02:  # 2% de error en name, email y signup_date
            name = None if random.random() < 0.02 else name
            email = None if random.random() < 0.02 else email
            signup_date = None if random.random() < 0.02 else signup_date
        
        # Introducir duplicados
        if random.random() < 0.1:  # 10% de duplicados
            data.append(data[random.randint(0, len(data)-1)])
        
        data.append([id, name, email, age, signup_date])

    df = pd.DataFrame(data, columns=["id", "name", "email", "age", "signup_date"])
    
    # Guardar en CSV
    df.to_csv('messy_data.csv', index=False)
    print("\n\n\n")
    print(df)
    print("\n\n\n")
    print("Datos generados y guardados en 'messy_data.csv'")
    return "datos_generados"