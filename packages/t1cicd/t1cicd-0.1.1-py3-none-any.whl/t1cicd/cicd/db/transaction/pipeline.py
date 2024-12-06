from uuid import UUID

from psycopg_pool import AsyncConnectionPool

from t1cicd.cicd.db.context.pipeline import PipelineCreateContext
from t1cicd.cicd.db.db import DB
from t1cicd.cicd.db.model.job import Job, JobCreate
from t1cicd.cicd.db.model.pipeline import PipelineCreate
from t1cicd.cicd.db.model.stage import Stage, StageCreate
from t1cicd.cicd.db.repository.job import JobRepository
from t1cicd.cicd.db.repository.pipeline import PipelineRepository
from t1cicd.cicd.db.repository.stage import StageRepository
from t1cicd.cicd.db.transaction.base import BaseTransaction
from t1cicd.cicd.parser.pipeline import ParsedPipeline


class PipelineTransaction(BaseTransaction):
    def __init__(self, pool: AsyncConnectionPool):
        super().__init__(pool)
        self.pipeline_repo = DB.get_repository(PipelineRepository)
        self.stage_repo = DB.get_repository(StageRepository)
        self.job_repo = DB.get_repository(JobRepository)

    async def create_new_pipeline(
        self, parsed_pipeline: ParsedPipeline, context: PipelineCreateContext
    ) -> tuple[UUID, int]:
        async with self.get_transaction():

            pipeline = await self.pipeline_repo.create(
                PipelineCreate(
                    git_branch=context.git_branch,
                    git_hash=context.git_hash,
                    git_comment=context.git_comment,
                    repo_url=context.repo_url,
                    pipeline_name=parsed_pipeline.pipeline_name,
                )
            )
            for stage_order, (stage_name, parsed_jobs) in enumerate(
                parsed_pipeline.get_all_stages()
            ):
                stage = await self.stage_repo.create(
                    StageCreate(
                        stage_name=stage_name,
                        pipeline_id=pipeline.id,
                        stage_order=stage_order,
                    )
                )
                # TODO - Add job order
                for job_order, job in enumerate(parsed_jobs):
                    await self.job_repo.create(
                        JobCreate(
                            stage_id=stage.id,
                            job_name=job.name,
                            job_order=job_order,
                            allow_failure=job.allow_failure,
                        )
                    )

            return pipeline.id, pipeline.run_id

    async def get_all_jobs(self, pipeline_id: UUID) -> dict[str, Job]:
        async with self.get_transaction():
            pipeline = await self.pipeline_repo.get(pipeline_id)
            stage_ids = pipeline.stage_ids
            jobs: dict[str, Job] = {}
            for stage_id in stage_ids:
                stage = await self.stage_repo.get(stage_id)
                for job_id in stage.job_ids:
                    job = await self.job_repo.get(job_id)
                    jobs[job.job_name] = job
            return jobs

    async def get_all_stages(self, pipeline_id: UUID) -> dict[str, Stage]:
        async with self.get_transaction():
            pipeline = await self.pipeline_repo.get(pipeline_id)
            stage_ids = pipeline.stage_ids
            stages: dict[str, Stage] = {}
            for stage_id in stage_ids:
                stage = await self.stage_repo.get(stage_id)
                stages[stage.stage_name] = stage
            return stages
