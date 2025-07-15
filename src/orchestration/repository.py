from dagster import repository
from pipeline import tenx_pipeline, schedule

@repository
def tenx_repository():
    return [tenx_pipeline, schedule]