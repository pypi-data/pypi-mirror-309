from uuid import UUID

from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool

from t1cicd.cicd.db.model.pipeline import Pipeline, PipelineCreate
from t1cicd.cicd.db.repository.base import BaseRepository


class PipelineRepository(BaseRepository[Pipeline, PipelineCreate]):

    def __init__(self, pool: AsyncConnectionPool):
        super().__init__(pool)

    async def create(self, item: PipelineCreate) -> Pipeline:
        query = """
        INSERT INTO pipelines (
            git_branch, git_hash, git_comment,status,pipeline_name, repo_url
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Pipeline)) as cur:
                result = await cur.execute(
                    query,
                    (
                        item.git_branch,
                        item.git_hash,
                        item.git_comment,
                        item.status,
                        item.pipeline_name,
                        item.repo_url,
                    ),
                )

                return await result.fetchone()

    async def get(self, id: UUID) -> Pipeline | None:

        query = """
        SELECT p.*,
            COALESCE(
                (SELECT array_agg(s.id ORDER BY s.stage_order)
                 FROM stages s 
                 WHERE s.pipeline_id = p.id),
                ARRAY[]::uuid[]
            ) as stage_ids
        FROM pipelines p 
        WHERE p.id = %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Pipeline)) as cur:
                result = await cur.execute(query, (id,))
                return await result.fetchone()

    async def get_by_run_id(self, run_id: int) -> Pipeline | None:
        query = """
        SELECT p.*,
            COALESCE(
                (SELECT array_agg(s.id ORDER BY s.stage_order)
                 FROM stages s 
                 WHERE s.pipeline_id = p.id),
                ARRAY[]::uuid[]
            ) as stage_ids
        FROM pipelines p 
        WHERE p.run_id = %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Pipeline)) as cur:
                result = await cur.execute(query, (run_id,))
                return await result.fetchone()

    async def update(self, item: Pipeline) -> Pipeline | None:
        update_fields = item.model_dump(
            exclude={"id", "created_at", "stage_ids"}, exclude_none=True
        )
        if not update_fields:
            return await self.get(item.id)
        set_clauses = [f"{field} = %s" for field in update_fields.keys()]
        params = list(update_fields.values())
        params.append(item.id)

        query = f"""
        UPDATE pipelines
        SET {', '.join(set_clauses)}
        WHERE id = %s
        RETURNING *
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Pipeline)) as cur:
                result = await cur.execute(query, params)
                return await result.fetchone()

    async def delete(self, id: UUID) -> bool:
        query = """
        DELETE FROM pipelines WHERE id = %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (id,))
                return cur.rowcount > 0

    async def get_all(self, limit: int, offset: int) -> list[Pipeline]:
        query = """
        SELECT p.*,
            COALESCE(
                (SELECT array_agg(s.id ORDER BY s.stage_order)
                 FROM stages s 
                 WHERE s.pipeline_id = p.id),
                ARRAY[]::uuid[]
            ) as stage_ids
        FROM pipelines p 
        ORDER BY p.created_at DESC
        LIMIT %s OFFSET %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Pipeline)) as cur:
                result = await cur.execute(query, (limit, offset))
                return await result.fetchall()

    async def get_by_repo_url(self, repo_url: str) -> list[Pipeline]:
        query = """
        SELECT p.*,
            COALESCE(
                (SELECT array_agg(s.id ORDER BY s.stage_order)
                 FROM stages s 
                 WHERE s.pipeline_id = p.id),
                ARRAY[]::uuid[]
            ) as stage_ids
        FROM pipelines p 
        WHERE p.repo_url = %s
        ORDER BY p.created_at DESC
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Pipeline)) as cur:
                result = await cur.execute(query, (repo_url,))
                return await result.fetchall()
