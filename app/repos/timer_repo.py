from typing import Optional
from uuid import UUID
import asyncpg

from app.models.timer import Timer


class TimerRepository:
    """Data access layer for Timer entities."""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        query = """
            INSERT INTO timers (duration, elapsed_time, status, urgency_level)
            VALUES ($1, $2, $3, $4)
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        row = await self.pool.fetchrow(query, duration, 0, "idle", 0)
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=row["status"],
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
        row = await self.pool.fetchrow(query, timer_id)
        if not row:
            return None
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=row["status"],
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def get_all(self) -> list[Timer]:
        """Fetch all timers."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            ORDER BY created_at DESC
        """
        rows = await self.pool.fetch(query)
        return [
            Timer(
                id=row["id"],
                duration=row["duration"],
                elapsed_time=row["elapsed_time"],
                status=row["status"],
                urgency_level=row["urgency_level"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

    async def update(self, timer: Timer) -> Timer:
        """Update timer state."""
        query = """
            UPDATE timers
            SET duration = $2, elapsed_time = $3, status = $4, urgency_level = $5, updated_at = now()
            WHERE id = $1
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        row = await self.pool.fetchrow(
            query,
            timer.id,
            timer.duration,
            timer.elapsed_time,
            timer.status,
            timer.urgency_level,
        )
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=row["status"],
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def delete(self, timer_id: UUID) -> bool:
        """Delete a timer by ID."""
        query = "DELETE FROM timers WHERE id = $1"
        result = await self.pool.execute(query, timer_id)
        return result == "DELETE 1"
