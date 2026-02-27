from uuid import UUID, uuid4
from datetime import datetime
import asyncpg
from app.models.timer import Timer, TimerStatus


class TimerRepo:
    """Data access for the timers table. All queries are parameterized."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create(self, duration: int) -> Timer:
        """Insert a new timer with idle status and elapsed_time=0. Return Timer model."""
        query = """
            INSERT INTO timers (id, duration, elapsed_time, status, urgency_level, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        now = datetime.utcnow()
        timer_id = uuid4()
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                timer_id,
                duration,
                0,  # elapsed_time
                TimerStatus.idle.value,
                0,  # urgency_level
                now,
                now,
            )
        return Timer(**dict(row))

    async def get_by_id(self, timer_id: UUID) -> Timer | None:
        """Fetch timer by ID. Return Timer model or None."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            WHERE id = $1
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id)
        if row is None:
            return None
        return Timer(**dict(row))

    async def list_all(self) -> list[Timer]:
        """Fetch all timers. Return list of Timer models."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            ORDER BY created_at DESC
        """
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [Timer(**dict(row)) for row in rows]

    async def update(
        self,
        timer_id: UUID,
        elapsed_time: int,
        status: TimerStatus,
        urgency_level: int,
    ) -> Timer | None:
        """Update timer fields and return updated Timer model or None if not found."""
        query = """
            UPDATE timers
            SET elapsed_time = $2, status = $3, urgency_level = $4, updated_at = $5
            WHERE id = $1
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        now = datetime.utcnow()
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                timer_id,
                elapsed_time,
                status.value,
                urgency_level,
                now,
            )
        if row is None:
            return None
        return Timer(**dict(row))
