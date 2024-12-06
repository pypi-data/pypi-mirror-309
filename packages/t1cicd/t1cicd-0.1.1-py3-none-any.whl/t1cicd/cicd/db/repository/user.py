from uuid import UUID

from psycopg.rows import class_row

from t1cicd.cicd.db.model.user import User, UserCreate
from t1cicd.cicd.db.repository.base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate]):
    async def create(self, item: UserCreate) -> User:
        query = """
        INSERT INTO users (username, email)
        VALUES (%s, %s)
        RETURNING *
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                result = await cur.execute(query, (item.username, item.email))
                return await result.fetchone()

    async def get(self, id: UUID) -> User | None:
        query = """
        SELECT * FROM users WHERE id = %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                result = await cur.execute(query, (id,))
                return await result.fetchone()

    async def update(self, item: User) -> User | None:
        update_fields = item.model_dump(exclude={"id"}, exclude_none=True)
        if not update_fields:
            return await self.get(item.id)
        set_clauses = [f"{field} = %s" for field in update_fields.keys()]
        params = list(update_fields.values())
        params.append(item.id)

        query = f"""
        UPDATE users
        SET {', '.join(set_clauses)}
        WHERE id = %s
        RETURNING *
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                result = await cur.execute(query, params)
                return await result.fetchone()

    async def delete(self, id: UUID) -> bool:
        query = """
        DELETE FROM users WHERE id = %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (id,))
                return cur.rowcount > 0
