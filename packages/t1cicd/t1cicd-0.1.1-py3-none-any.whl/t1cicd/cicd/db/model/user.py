from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime | None
    updated_at: datetime | None


class UserCreate(BaseModel):
    username: str
    email: str
