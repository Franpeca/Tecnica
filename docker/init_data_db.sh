#!/bin/bash

# Permite crear las tablas en caso de que no existan

# Esperar a que el servidor de PostgreSQL esté disponible
until psql -U user -d postgres -c '\q'; do
  echo "Esperando a que PostgreSQL esté disponible..."
  sleep 2
done

# Crear la base de datos si no existe
DB_EXISTS=$(psql -U user -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='data_db'")
if [ -z "$DB_EXISTS" ]; then
  echo "Creando la base de datos 'data_db'..."
  psql -U user -d postgres -c "CREATE DATABASE data_db;"
else
  echo "La base de datos 'data_db' ya existe."
fi

# Crear la tabla si no existe
psql -U user -d data_db -c "
CREATE TABLE IF NOT EXISTS clean_data (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    age INT,
    signup_date DATE
);
"