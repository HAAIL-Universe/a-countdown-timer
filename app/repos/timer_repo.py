from typing import Any
from uuid import UUID, uuid4
from datetime import datetime
import asyncpg

from app.models.timer import Timer, TimerStatus


class TimerRepo:
    """Data access for the timers table. All queries are parameterized."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create(self, duration: int) -> Timer:
        """Create a new timer with idle status and zero elapsed time."""
        timer_id = uuid4()
        now = datetime.utcnow()
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
                0,
                TimerStatus.idle.value,
                0,
                now,
                now,
            )
        return self._row_to_timer(row)

    async def get_by_id(self, timer_id: UUID) -> Timer | None:
        """Fetch a timer by ID."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            WHERE id = $1
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id)
        return self._row_to_timer(row) if row else None

    async def list_all(self) -> list[Timer]:
        """List all timers ordered by creation date descending."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            ORDER BY created_at DESC
        """
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [self._row_to_timer(r) for r in rows]

    async def update(
        self,
        timer_id: UUID,
        elapsed_time: int,
        status: TimerStatus,
        urgency_level: int,
    ) -> Timer | None:
        """Update a timer's elapsed_time, status, and urgency_level."""
        now = datetime.utcnow()
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
        return self._row_to_timer(row) if row else None

    @staticmethod
    def _row_to_timer(row: asyncpg.Record) -> Timer:
        """Convert asyncpg Row to Timer Pydantic model."""
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=TimerStatus(row["status"]),
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
