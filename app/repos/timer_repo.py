from uuid import UUID
import asyncpg
from app.models.timer import Timer, TimerStatus


class TimerRepo:
    """Data access layer for the timers table. All queries are parameterized."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create(self, duration: int) -> Timer:
        """Insert a new timer with idle status and zero elapsed time."""
        query = """
            INSERT INTO timers (duration, elapsed_time, status, urgency_level)
            VALUES ($1, $2, $3, $4)
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, duration, 0, TimerStatus.idle.value, 0)
        return Timer(**dict(row))

    async def get_by_id(self, timer_id: UUID) -> Timer | None:
        """Fetch a timer by ID. Returns None if not found."""
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
        """Fetch all timers ordered by creation time (newest first)."""
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
        """Update a timer's elapsed_time, status, and urgency_level. Returns updated Timer or None if not found."""
        query = """
            UPDATE timers
            SET elapsed_time = $2, status = $3, urgency_level = $4, updated_at = NOW()
            WHERE id = $1
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id, elapsed_time, status.value, urgency_level)
        if row is None:
            return None
        return Timer(**dict(row))
