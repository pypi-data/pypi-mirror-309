from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"


class Job(BaseModel):
    id: UUID
    stage_id: UUID
    job_name: str
    job_order: int
    status: JobStatus = JobStatus.PENDING
    start_time: datetime | None
    end_time: datetime | None
    retry_count: int = 0
    created_at: datetime
    updated_at: datetime
    artifact_ids: list[UUID] = []
    allow_failure: bool = False


class JobCreate(BaseModel):
    stage_id: UUID
    job_name: str
    job_order: int
    allow_failure: bool = False
