from datetime import datetime
from uuid import UUID

import asyncpg
from pydantic import ValidationError

from app.models.timer import Timer, TimerStatus


class TimerRepository:
    """Data access layer for Timer entities."""

    def __init__(self, pool: asyncpg.Pool):
        """Initialize with asyncpg connection pool."""
        self.pool = pool

    async def create(self, timer: Timer) -> Timer:
        """Create a new timer in the database."""
        now = datetime.utcnow()
        query = """
            INSERT INTO timers (duration, elapsed_time, status, urgency_level, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                timer.duration,
                timer.elapsed_time,
                timer.status.value,
                timer.urgency_level,
                now,
                now,
            )
        if not row:
            raise RuntimeError("Failed to create timer")
        return self._row_to_timer(row)

    async def get_by_id(self, timer_id: UUID) -> Timer | None:
        """Fetch timer by ID."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            WHERE id = $1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id)
        if not row:
            return None
        return self._row_to_timer(row)

    async def list_all(self) -> list[Timer]:
        """Fetch all timers."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            ORDER BY created_at DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [self._row_to_timer(row) for row in rows]

    async def update(self, timer: Timer) -> Timer:
        """Update an existing timer."""
        now = datetime.utcnow()
        query = """
            UPDATE timers
            SET duration = $1, elapsed_time = $2, status = $3, urgency_level = $4, updated_at = $5
            WHERE id = $6
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                timer.duration,
                timer.elapsed_time,
                timer.status.value,
                timer.urgency_level,
                now,
                timer.id,
            )
        if not row:
            raise RuntimeError(f"Timer {timer.id} not found")
        return self._row_to_timer(row)

    async def delete(self, timer_id: UUID) -> bool:
        """Delete a timer by ID."""
        query = "DELETE FROM timers WHERE id = $1"
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, timer_id)
        return result == "DELETE 1"

    @staticmethod
    def _row_to_timer(row: asyncpg.Record) -> Timer:
        """Convert database row to Timer model."""
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=TimerStatus(row["status"]),
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
