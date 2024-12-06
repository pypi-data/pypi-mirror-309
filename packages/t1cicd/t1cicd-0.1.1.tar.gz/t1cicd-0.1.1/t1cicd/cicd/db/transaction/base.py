import contextlib

from psycopg_pool import AsyncConnectionPool


class BaseTransaction:
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    @contextlib.asynccontextmanager
    async def get_transaction(self):
        """Context manager for handling transaction with connection from pool."""
        async with self.pool.connection() as conn:
            async with conn.transaction():
                yield conn
