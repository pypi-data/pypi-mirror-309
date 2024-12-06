from pydantic import BaseModel

"""
This module defines data models for representing CI/CD pipeline run details and summaries using Pydantic.

Classes:
    Status (str): Enum-like class representing the status of a pipeline, stage, or job.
        Attributes:
            SUCCESS (str): Indicates a successful run.
            FAILED (str): Indicates a failed run.
            CANCELED (str): Indicates a canceled run.

    RepoRunSummary (BaseModel): Model representing a summary of a repository run.
        Attributes:
            pipeline_name (str): Name of the pipeline.
            run_number (int): Run number of the pipeline.
            git_commit_hash (str): Git commit hash associated with the run.
            status (Status): Status of the run.
            start_time (datetime): Start time of the run.
            completion_time (datetime): Completion time of the run.

    RepoRunSummaryResponse (BaseModel): Model representing a response containing multiple repository run summaries.
        Attributes:
            runs (List[RepoRunSummary]): List of repository run summaries.

    StageSummaryForPipeline (BaseModel): Model representing a summary of a stage within a pipeline.
        Attributes:
            stage_name (str): Name of the stage.
            stage_status (Status): Status of the stage.
            start_time (datetime): Start time of the stage.
            completion_time (datetime): Completion time of the stage.

    PipelineRunDetail (BaseModel): Model representing detailed information about a pipeline run.
        Attributes:
            pipeline_name (str): Name of the pipeline.
            run_number (int): Run number of the pipeline.
            git_commit_hash (str): Git commit hash associated with the run.
            pipeline_status (Status): Status of the pipeline run.
            stages (List[StageSummaryForPipeline]): List of stage summaries for the pipeline.

    PipelineRunDetailResponse (BaseModel): Model representing a response containing detailed information about a pipeline run.
        Attributes:
            pipeline_run (PipelineRunDetail): Detailed information about the pipeline run.

    JobSummaryForStage (BaseModel): Model representing a summary of a job within a stage.
        Attributes:
            job_name (str): Name of the job.
            job_status (Status): Status of the job.
            allows_failure (bool): Indicates if the job allows failure.
            start_time (datetime): Start time of the job.
            completion_time (datetime): Completion time of the job.

    StageRunDetail (BaseModel): Model representing detailed information about a stage run.
        Attributes:
            pipeline_name (str): Name of the pipeline.
            run_number (int): Run number of the pipeline.
            git_commit_hash (str): Git commit hash associated with the run.
            stage_name (str): Name of the stage.
            stage_status (Status): Status of the stage run.
            jobs (List[JobSummaryForStage]): List of job summaries for the stage.

    StageRunDetailResponse (BaseModel): Model representing a response containing detailed information about a stage run.
        Attributes:
            stage_run (StageRunDetail): Detailed information about the stage run.

    StageAllRunsResponse (BaseModel): Model representing a response containing multiple stage run details.
        Attributes:
            stage_runs (List[StageRunDetail]): List of stage run details.

    JobRunDetail (BaseModel): Model representing detailed information about a job run.
        Attributes:
            pipeline_name (str): Name of the pipeline.
            run_number (int): Run number of the pipeline.
            git_commit_hash (str): Git commit hash associated with the run.
            stage_name (str): Name of the stage.
            job_name (str): Name of the job.
            job_status (Status): Status of the job run.
            allows_failure (bool): Indicates if the job allows failure.
            start_time (datetime): Start time of the job run.
            completion_time (datetime): Completion time of the job run.

    JobRunDetailResponse (BaseModel): Model representing a response containing detailed information about a job run.
        Attributes:
            job_run (JobRunDetail): Detailed information about the job run.

    JobAllRunsResponse (BaseModel): Model representing a response containing multiple job run details.
        Attributes:
            job_runs (List[JobRunDetail]): List of job run details.
"""
from datetime import datetime
from enum import Enum
from typing import List


class Status(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"


class RepoRunSummary(BaseModel):
    pipeline_name: str
    run_number: int
    git_commit_hash: str
    status: Status
    start_time: datetime
    completion_time: datetime


class RepoRunSummaryResponse(BaseModel):
    runs: List[RepoRunSummary]


class StageSummaryForPipeline(BaseModel):
    stage_name: str
    stage_status: Status
    start_time: datetime
    completion_time: datetime


class PipelineRunDetail(BaseModel):
    pipeline_name: str
    run_number: int
    git_commit_hash: str
    pipeline_status: Status
    stages: List[StageSummaryForPipeline]


class PipelineRunDetailResponse(BaseModel):
    pipeline_runs: List[PipelineRunDetail]


class JobSummaryForStage(BaseModel):
    job_name: str
    job_status: Status
    allows_failure: bool
    start_time: datetime
    completion_time: datetime


class StageRunDetail(BaseModel):
    pipeline_name: str
    run_number: int
    git_commit_hash: str
    stage_name: str
    stage_status: Status
    jobs: List[JobSummaryForStage]


class StageRunDetailResponse(BaseModel):
    stage_run: StageRunDetail


class StageAllRunsResponse(BaseModel):
    stage_runs: List[StageRunDetail]


class JobRunDetail(BaseModel):
    pipeline_name: str
    run_number: int
    git_commit_hash: str
    stage_name: str
    job_name: str
    job_status: Status
    allows_failure: bool
    start_time: datetime
    completion_time: datetime


class JobRunDetailResponse(BaseModel):
    job_run: JobRunDetail


class JobAllRunsResponse(BaseModel):
    job_runs: List[JobRunDetail]


# Dummy data for testing
repo_run_summary = RepoRunSummary(
    pipeline_name="pipeline-example",
    run_number=1,
    git_commit_hash="ABCDEFGH",
    status=Status.SUCCESS,
    start_time=datetime(2024, 10, 21, 9, 0, 0),
    completion_time=datetime(2024, 10, 21, 9, 2, 0),
)

stage_summary = StageSummaryForPipeline(
    stage_name="build",
    stage_status=Status.SUCCESS,
    start_time=datetime(2024, 10, 21, 9, 0, 0),
    completion_time=datetime(2024, 10, 21, 9, 1, 0),
)

pipeline_run_detail = PipelineRunDetail(
    pipeline_name="pipeline-example",
    run_number=1,
    git_commit_hash="ABCDEFGH",
    pipeline_status=Status.SUCCESS,
    stages=[stage_summary],
)

job_summary = JobSummaryForStage(
    job_name="unit-tests",
    job_status=Status.SUCCESS,
    allows_failure=False,
    start_time=datetime(2024, 10, 21, 9, 0, 0),
    completion_time=datetime(2024, 10, 21, 9, 1, 0),
)

stage_run_detail = StageRunDetail(
    pipeline_name="pipeline-example",
    run_number=1,
    git_commit_hash="ABCDEFGH",
    stage_name="build",
    stage_status=Status.SUCCESS,
    jobs=[job_summary],
)

job_run_detail = JobRunDetail(
    pipeline_name="pipeline-example",
    run_number=1,
    git_commit_hash="ABCDEFGH",
    stage_name="build",
    job_name="unit-tests",
    job_status=Status.SUCCESS,
    allows_failure=False,
    start_time=datetime(2024, 10, 21, 9, 0, 0),
    completion_time=datetime(2024, 10, 21, 9, 1, 0),
)

repo_run_summary_response = RepoRunSummaryResponse(runs=[repo_run_summary])

pipeline_run_detail_response = PipelineRunDetailResponse(
    pipeline_runs=[pipeline_run_detail]
)

stage_run_detail_response = StageAllRunsResponse(stage_runs=[stage_run_detail])

job_run_detail_response = JobAllRunsResponse(job_runs=[job_run_detail])
