from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Artifact(BaseModel):
    id: UUID
    job_id: UUID
    file_path: str
    file_size: int
    created_at: datetime
    expiry_date: datetime | None


class ArtifactCreate(BaseModel):
    job_id: UUID
    file_path: str
    file_size: int
    expiry_date: datetime | None = None
