from typing import Any
from uuid import UUID
import asyncpg
from datetime import datetime
from app.models.timer import Timer, TimerStatus


class TimerRepo:
    """Repository for Timer CRUD operations. All queries are parameterized."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create(self, duration: int) -> Timer:
        """Insert a new timer with status=idle, elapsed_time=0. Return Timer with UUID."""
        query = """
            INSERT INTO timers (duration, elapsed_time, status, urgency_level, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        now = datetime.utcnow()
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                duration,
                0,  # elapsed_time
                TimerStatus.idle.value,
                0,  # urgency_level
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
        """List all timers."""
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
        """Update timer state (elapsed_time, status, urgency_level)."""
        query = """
            UPDATE timers
            SET elapsed_time = $1, status = $2, urgency_level = $3, updated_at = $4
            WHERE id = $5
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        now = datetime.utcnow()
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
        """Convert asyncpg.Record to Timer model."""
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=TimerStatus(row["status"]),
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
