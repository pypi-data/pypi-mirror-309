from t1cicd.cicd.db.model.job import Job
from t1cicd.cicd.db.model.pipeline import Pipeline
from t1cicd.cicd.db.model.stage import Stage
from t1cicd.cicd.db.transform.base import ModelRelationship


class TransformFactory:
    @staticmethod
    def create_pipeline_stage_relationship() -> ModelRelationship[Pipeline, Stage]:
        return ModelRelationship(
            parent_model=Pipeline, related_model=Stage, related_ids_field="stage_ids"
        )

    @staticmethod
    def create_stage_job_relationship() -> ModelRelationship[Stage, Job]:
        return ModelRelationship(
            parent_model=Stage, related_model=Job, related_ids_field="job_ids"
        )

    @staticmethod
    def create_pipeline_stage_job_relationship() -> ModelRelationship[Pipeline, Stage]:
        stage_job_summary = TransformFactory.create_stage_job_relationship()
        return ModelRelationship(
            parent_model=Pipeline,
            related_model=Stage,
            related_ids_field="stage_ids",
            nested_relationship=stage_job_summary,
        )
