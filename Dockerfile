# Establecer la base de la imagen
ARG BASE_IMAGE=python:3.12.3-slim
FROM $BASE_IMAGE AS runtime-environment

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless && \
    rm -rf /var/lib/apt/lists/*

# Actualizar pip y otras dependencias
RUN python -m pip install -U "pip>=21.2"
RUN pip install uv

# Copiar el requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN uv pip install --system --no-cache-dir -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

# Crear un usuario para Kedro
ARG KEDRO_UID=999
ARG KEDRO_GID=0
RUN groupadd -f -g ${KEDRO_GID} kedro_group && \
    useradd -m -d /home/kedro_docker -s /bin/bash -g ${KEDRO_GID} -u ${KEDRO_UID} kedro_docker

WORKDIR /home/kedro_docker
USER kedro_docker

# Exponer el puerto necesario
EXPOSE 8888