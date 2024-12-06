from typing import List

from pydantic import BaseModel, Field, model_validator

from t1cicd.cicd.parser.constants import DEFAULT_GLOBAL_KEYWORDS
from t1cicd.cicd.parser.job import ParsedJob
from t1cicd.cicd.parser.stage import ParsedStage
from t1cicd.cicd.parser.utils import get_dry_run_order


class ParsedPipeline(BaseModel):
    """
    The parsed pipeline corresponds to the content of YAML file

    """

    pipeline_name: str = Field(..., description="The name of the pipeline")
    parsed_stages: ParsedStage = Field(..., description="The stages to run")
    variables: dict = Field(..., description="The variables to use in the pipeline")

    @model_validator(mode="before")
    def populate_variables(cls, values):
        # Check each field and populate from variables if None
        parsed_stages = values.get("parsed_stages")
        variables = values.get("variables")

        # Populate job fields with variables if they are None
        for stage_name, jobs in parsed_stages.stages.items():
            for job in jobs:
                for keyword in DEFAULT_GLOBAL_KEYWORDS:
                    if (getattr(job, keyword, None) is None) and (keyword in variables):
                        setattr(job, keyword, variables[keyword])

        return values

    def get_jobs_in_stage(self, stage_name: str) -> list:
        return self.parsed_stages.get_jobs_in_stage(stage_name)

    def get_all_stage_names(self) -> list:
        return self.parsed_stages.get_all_stage_names()

    def get_all_jobs(self) -> dict[str, List[ParsedJob]]:
        return self.parsed_stages.stages

    def get_all_stages(self) -> list[tuple[str, List[ParsedJob]]]:
        return self.parsed_stages.get_all_stages()

    def dry_run(self):
        dry_run_order = get_dry_run_order(self.parsed_stages.stages)
        order = 0
        for stage in dry_run_order:
            for jobs in stage:
                print(f"{order}: {jobs}")
                order += 1

    # Execute the pipeline for now. This will be discarded and replaced by the actual execution in the future
    def execute_pipeline(self):
        for stage_name in self.get_all_stage_names():
            print(f"Executing Stage: {stage_name}")
            sorted_jobs = self.parsed_stages.get_sorted_jobs_in_stage(stage_name)
            for job in sorted_jobs:
                self.execute_job(job)

    def execute_job(self, job: ParsedJob):
        print(f"Executing Job: {job.name}")

        if isinstance(job.script, list):
            for command in job.script:
                print(f"Running command: {command}")
        else:
            print(f"Running command: {job.script}")
        print(f"Job {job.name} completed.\n")
