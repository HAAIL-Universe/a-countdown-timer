from uuid import UUID
from typing import Optional, List
from datetime import datetime
import asyncpg
from app.models.timer import Timer


class TimerRepository:
    """Repository for Timer persistence."""

    def __init__(self, pool: asyncpg.Pool):
        """Initialize with asyncpg connection pool."""
        self.pool = pool

    async def create(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        query = """
            INSERT INTO timers (duration, elapsed_time, status, urgency_level, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        now = datetime.utcnow()
        row = await self.pool.fetchrow(
            query,
            duration,
            0,
            "idle",
            0,
            now,
            now,
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

    async def get_by_id(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch timer by ID."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            WHERE id = $1
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

    async def list_all(self) -> List[Timer]:
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

    async def update(self, timer_id: UUID, timer: Timer) -> Optional[Timer]:
        """Update timer and return updated row."""
        query = """
            UPDATE timers
            SET duration = $1, elapsed_time = $2, status = $3, urgency_level = $4, updated_at = $5
            WHERE id = $6
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        now = datetime.utcnow()
        row = await self.pool.fetchrow(
            query,
            timer.duration,
            timer.elapsed_time,
            timer.status,
            timer.urgency_level,
            now,
            timer_id,
        )
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

    async def delete(self, timer_id: UUID) -> bool:
        """Delete timer by ID."""
        query = "DELETE FROM timers WHERE id = $1"
        result = await self.pool.execute(query, timer_id)
        return result == "DELETE 1"
