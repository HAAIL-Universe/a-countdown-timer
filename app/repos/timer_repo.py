from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.timer import Timer, TimerStatus


class TimerRepo:
    """Repository for Timer persistence."""

    def __init__(self, db_pool):
        """Initialize with database connection pool."""
        self.db_pool = db_pool

    async def create(self, timer: Timer) -> Timer:
        """Create a new timer in the database."""
        query = """
        INSERT INTO timers (id, duration, elapsed_time, status, urgency_level, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                timer.id,
                timer.duration,
                timer.elapsed_time,
                timer.status.value,
                timer.urgency_level,
                timer.created_at,
                timer.updated_at,
            )
            if row:
                return Timer(
                    id=row["id"],
                    duration=row["duration"],
                    elapsed_time=row["elapsed_time"],
                    status=TimerStatus(row["status"]),
                    urgency_level=row["urgency_level"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
            raise RuntimeError("Failed to create timer")

    async def get_by_id(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch a timer by ID."""
        query = """
        SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        FROM timers
        WHERE id = $1
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id)
            if row:
                return Timer(
                    id=row["id"],
                    duration=row["duration"],
                    elapsed_time=row["elapsed_time"],
                    status=TimerStatus(row["status"]),
                    urgency_level=row["urgency_level"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
            return None

    async def get_all(self) -> list[Timer]:
        """Fetch all timers."""
        query = """
        SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        FROM timers
        ORDER BY created_at DESC
        """
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(query)
            timers = []
            for row in rows:
                timer = Timer(
                    id=row["id"],
                    duration=row["duration"],
                    elapsed_time=row["elapsed_time"],
                    status=TimerStatus(row["status"]),
                    urgency_level=row["urgency_level"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
                timers.append(timer)
            return timers

    async def update(self, timer: Timer) -> Timer:
        """Update an existing timer."""
        query = """
        UPDATE timers
        SET duration = $1, elapsed_time = $2, status = $3, urgency_level = $4, updated_at = $5
        WHERE id = $6
        RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                timer.duration,
                timer.elapsed_time,
                timer.status.value,
                timer.urgency_level,
                datetime.utcnow(),
                timer.id,
            )
            if row:
                return Timer(
                    id=row["id"],
                    duration=row["duration"],
                    elapsed_time=row["elapsed_time"],
                    status=TimerStatus(row["status"]),
                    urgency_level=row["urgency_level"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
            raise RuntimeError(f"Failed to update timer {timer.id}")

    async def delete(self, timer_id: UUID) -> bool:
        """Delete a timer by ID."""
        query = "DELETE FROM timers WHERE id = $1"
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(query, timer_id)
            return result == "DELETE 1"
