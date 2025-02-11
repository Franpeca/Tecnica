#!/bin/bash

# Espera a que pgAdmin esté listo
sleep 10

# Usa curl para interactuar con la API de pgAdmin y agregar la conexión
curl -X POST -d "name=data_db&host=postgres&port=5432&username=user&password=pass123&dbname=data_db" \
  http://admin:admin@localhost/api/servers/0/connections