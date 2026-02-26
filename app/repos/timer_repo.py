from datetime import datetime
from typing import Optional
from uuid import UUID

import asyncpg


class TimerRepository:
    """Repository for Timer persistence using asyncpg."""

    def __init__(self, pool: asyncpg.Pool):
        """Initialize repository with asyncpg connection pool."""
        self.pool = pool

    async def create(
        self,
        duration: int,
        elapsed_time: int = 0,
        status: str = "idle",
        urgency_level: int = 0,
    ) -> dict:
        """Create a new timer and return it."""
        now = datetime.utcnow()
        query = """
            INSERT INTO timers (duration, elapsed_time, status, urgency_level, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query, duration, elapsed_time, status, urgency_level, now, now
            )
        return dict(row) if row else None

    async def get_by_id(self, timer_id: UUID) -> Optional[dict]:
        """Fetch a timer by ID."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            WHERE id = $1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id)
        return dict(row) if row else None

    async def list_all(self) -> list[dict]:
        """Fetch all timers."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            ORDER BY created_at DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [dict(row) for row in rows]

    async def update(
        self,
        timer_id: UUID,
        duration: Optional[int] = None,
        elapsed_time: Optional[int] = None,
        status: Optional[str] = None,
        urgency_level: Optional[int] = None,
    ) -> Optional[dict]:
        """Update timer fields and return updated timer."""
        updates = []
        params = []
        param_index = 1

        if duration is not None:
            updates.append(f"duration = ${param_index}")
            params.append(duration)
            param_index += 1

        if elapsed_time is not None:
            updates.append(f"elapsed_time = ${param_index}")
            params.append(elapsed_time)
            param_index += 1

        if status is not None:
            updates.append(f"status = ${param_index}")
            params.append(status)
            param_index += 1

        if urgency_level is not None:
            updates.append(f"urgency_level = ${param_index}")
            params.append(urgency_level)
            param_index += 1

        if not updates:
            return await self.get_by_id(timer_id)

        updates.append(f"updated_at = ${param_index}")
        params.append(datetime.utcnow())
        params.append(timer_id)

        query = f"""
            UPDATE timers
            SET {', '.join(updates)}
            WHERE id = ${param_index + 1}
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *params)
        return dict(row) if row else None

    async def delete(self, timer_id: UUID) -> bool:
        """Delete a timer by ID."""
        query = "DELETE FROM timers WHERE id = $1"
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, timer_id)
        return result == "DELETE 1"
