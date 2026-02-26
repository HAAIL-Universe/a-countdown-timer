from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import asyncpg

from app.models.timer import Timer, TimerStatus


class TimerRepo:
    """Data access layer for Timer entities. All queries are parameterized."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        query = """
            INSERT INTO timers (id, duration, elapsed_time, status, urgency_level, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, now(), now())
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        timer_id = uuid4()
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id, duration, 0, "idle", 0)
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=TimerStatus(row["status"]),
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def get_by_id(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch a timer by ID."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers WHERE id = $1
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id)
        if not row:
            return None
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=TimerStatus(row["status"]),
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def list_all(self) -> list[Timer]:
        """Fetch all timers."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            ORDER BY created_at DESC
        """
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [
            Timer(
                id=row["id"],
                duration=row["duration"],
                elapsed_time=row["elapsed_time"],
                status=TimerStatus(row["status"]),
                urgency_level=row["urgency_level"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

    async def update(
        self,
        timer_id: UUID,
        elapsed_time: int,
        status: TimerStatus,
        urgency_level: int,
    ) -> Optional[Timer]:
        """Update timer state and return updated timer."""
        query = """
            UPDATE timers
            SET elapsed_time = $2, status = $3, urgency_level = $4, updated_at = now()
            WHERE id = $1
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id, elapsed_time, status.value, urgency_level)
        if not row:
            return None
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=TimerStatus(row["status"]),
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def delete(self, timer_id: UUID) -> bool:
        """Delete a timer by ID."""
        query = "DELETE FROM timers WHERE id = $1"
        async with self._pool.acquire() as conn:
            result = await conn.execute(query, timer_id)
        return result == "DELETE 1"
