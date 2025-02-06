# src/data_processing/data_pipeline.py
from kedro.pipeline import Pipeline, node
from data_processing.nodes.data_cleaning import clean_data
from data_processing.nodes.data_generation import generate_data


def data_pipeline() -> Pipeline:
    return Pipeline(
        [
            node(generate_data, inputs=None, outputs="dataset_generado", name="generar_datos"),
            node(clean_data, inputs="dataset_generado", outputs="dataset_limpiado", name="limpiar_datos"),
        ]
    )
