import asyncio
from typing import Type, TypeVar

from flask import Flask
from psycopg_pool import AsyncConnectionPool

from t1cicd.cicd.db.config import DBConfig
from t1cicd.cicd.db.repository.base import BaseRepository
from t1cicd.cicd.db.transaction.base import BaseTransaction

T = TypeVar("T")
TTransaction = TypeVar("TTransaction", bound="BaseTransaction")


class DB:
    _pool: AsyncConnectionPool | None = None
    _repositories: dict[str, BaseRepository] = {}
    _transactions: dict[str, BaseTransaction] = {}

    @classmethod
    async def init(cls, config: DBConfig):
        if cls._pool is None:
            pool = AsyncConnectionPool(
                min_size=config.min_size,
                max_size=config.max_size,
                conninfo=config.conninfo,
                open=False,
            )
            await pool.open()
            cls._pool = pool
            cls._repositories = {}
            cls._transactions = {}

    @classmethod
    async def close(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
            cls._repositories = {}
            cls._transactions = {}

    @classmethod
    def get_pool(cls) -> AsyncConnectionPool:
        if cls._pool is None:
            raise ValueError("DB not initialized")
        return cls._pool

    @classmethod
    def get_repository(cls, repo_class: Type[T]) -> T:
        repo_name = repo_class.__name__
        if repo_name not in cls._repositories:
            cls._repositories[repo_name] = repo_class(cls.get_pool())
        return cls._repositories[repo_name]

    @classmethod
    def get_transaction(cls, transaction_class: Type[TTransaction]) -> TTransaction:
        transaction_name = transaction_class.__name__
        if transaction_name not in cls._transactions:
            cls._transactions[transaction_name] = transaction_class(cls.get_pool())
        return cls._transactions[transaction_name]


def init_flask_db(app: Flask):
    # Initial setup remains the same
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _async_init():
        config = DBConfig.from_env()
        await DB.init(config)
        try:
            async with DB._pool.connection() as conn:
                await conn.execute("SELECT 1")
                app.logger.info("Database connection successful")
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")
            raise

    try:
        loop.run_until_complete(_async_init())
    finally:
        loop.close()

    # Fixed teardown handler
    @app.teardown_appcontext
    def shutdown_db(exception=None):
        # TODO
        print("shutdown_db")
