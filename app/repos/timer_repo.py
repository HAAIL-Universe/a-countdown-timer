from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

import asyncpg

from app.models.timer import Timer, TimerStatus


class TimerRepo:
    """Data access for the timers table. All queries are parameterized."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create(self, duration: int) -> Timer:
        """Insert a new timer with initial status=idle and elapsed_time=0."""
        timer_id = uuid4()
        now = datetime.now(timezone.utc)
        query = """
            INSERT INTO timers (id, duration, elapsed_time, status, urgency_level, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                timer_id,
                duration,
                0,  # elapsed_time
                TimerStatus.idle.value,  # status
                0,  # urgency_level
                now,
                now,
            )
        return Timer(**dict(row))

    async def get_by_id(self, timer_id: UUID) -> Timer | None:
        """Fetch a timer by id."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            WHERE id = $1
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id)
        if not row:
            return None
        return Timer(**dict(row))

    async def list_all(self) -> list[Timer]:
        """Fetch all timers ordered by creation date (newest first)."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            ORDER BY created_at DESC
        """
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [Timer(**dict(r)) for r in rows]

    async def update(
        self,
        timer_id: UUID,
        elapsed_time: int,
        status: TimerStatus,
        urgency_level: int,
    ) -> Timer | None:
        """Update timer fields and return the updated row."""
        now = datetime.now(timezone.utc)
        query = """
            UPDATE timers
            SET elapsed_time = $1, status = $2, urgency_level = $3, updated_at = $4
            WHERE id = $5
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                elapsed_time,
                status.value,
                urgency_level,
                now,
                timer_id,
            )
        if not row:
            return None
        return Timer(**dict(row))
