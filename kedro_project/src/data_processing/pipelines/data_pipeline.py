# src/data_processing/data_pipeline.py
from kedro.pipeline import Pipeline, node
from data_processing.nodes.data_cleaning import clean_data
from data_processing.nodes.data_generation import generate_data

# Aquí se genera la pipeline de Kedro para las dos funciones pedidas en la entrevista
# Se pueden definir más en otros ficheros, dando mucho juego
def data_pipeline() -> Pipeline:
    return Pipeline(
        [
            node(generate_data, inputs=None, outputs="messy_data", name="generar_datos"),
            node(clean_data, inputs="messy_data", outputs="clean_data", name="limpiar_datos"),
        ]
    )
