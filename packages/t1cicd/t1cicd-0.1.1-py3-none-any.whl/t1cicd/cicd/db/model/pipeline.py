from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class PipelineStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"


class PipelineCreate(BaseModel):
    git_branch: str
    git_hash: str
    git_comment: str
    pipeline_name: str
    repo_url: str
    status: PipelineStatus = PipelineStatus.PENDING
    # user_id: UUID


class Pipeline(BaseModel):
    id: UUID
    run_id: int
    pipeline_name: str
    repo_url: str
    git_branch: str
    git_hash: str
    git_comment: str
    status: PipelineStatus
    running_time: float | None
    start_time: datetime | None
    end_time: datetime | None
    created_at: datetime
    stage_ids: list[UUID] = []
    # user_id: UUID
