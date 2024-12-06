from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from psycopg_pool import AsyncConnectionPool

T = TypeVar("T")
CreateT = TypeVar("CreateT")


class BaseRepository(ABC, Generic[T, CreateT]):
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    @abstractmethod
    async def create(self, item: CreateT) -> T:
        pass

    @abstractmethod
    async def get(self, id: UUID) -> T | None:
        pass

    @abstractmethod
    async def update(self, item: T) -> T | None:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        pass
