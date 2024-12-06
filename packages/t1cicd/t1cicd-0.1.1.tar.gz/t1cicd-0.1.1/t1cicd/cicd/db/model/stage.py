from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class StageStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"


class Stage(BaseModel):
    id: UUID
    pipeline_id: UUID
    stage_name: str
    status: StageStatus
    start_time: datetime | None
    end_time: datetime | None
    stage_order: int
    created_at: datetime | None
    updated_at: datetime | None
    job_ids: list[UUID] = []


class StageCreate(BaseModel):
    pipeline_id: UUID
    stage_name: str
    stage_order: int
