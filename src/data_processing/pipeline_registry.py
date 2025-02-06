from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from data_processing.pipelines.data_pipeline import data_pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines."""
    
    pipelines = {
        "__default__": data_pipeline(),  # Asigna la pipeline a la clave "__default__"
    }
    
    return pipelines
