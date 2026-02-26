from typing import List, Optional
from uuid import UUID
import asyncpg
from datetime import datetime
from app.models import Timer


class TimerRepository:
    """Repository for Timer data access."""

    def __init__(self, pool: asyncpg.Pool):
        """Initialize with asyncpg connection pool."""
        self.pool = pool

    async def create(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO timers (duration, elapsed_time, status, urgency_level, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
                """,
                duration,
                0,
                "idle",
                0,
                datetime.utcnow(),
                datetime.utcnow(),
            )
            return self._row_to_timer(row)

    async def get_by_id(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch timer by ID."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at FROM timers WHERE id = $1",
                timer_id,
            )
            return self._row_to_timer(row) if row else None

    async def get_all(self) -> List[Timer]:
        """Fetch all timers."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at FROM timers ORDER BY created_at DESC"
            )
            return [self._row_to_timer(row) for row in rows]

    async def update(self, timer: Timer) -> Timer:
        """Update an existing timer."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                UPDATE timers
                SET duration = $2, elapsed_time = $3, status = $4, urgency_level = $5, updated_at = $6
                WHERE id = $1
                RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
                """,
                timer.id,
                timer.duration,
                timer.elapsed_time,
                timer.status,
                timer.urgency_level,
                datetime.utcnow(),
            )
            return self._row_to_timer(row)

    async def delete(self, timer_id: UUID) -> bool:
        """Delete a timer by ID."""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM timers WHERE id = $1",
                timer_id,
            )
            return result == "DELETE 1"

    def _row_to_timer(self, row: asyncpg.Record) -> Timer:
        """Convert database row to Timer model."""
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=row["status"],
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
