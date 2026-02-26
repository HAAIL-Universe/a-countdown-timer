from typing import Optional
from uuid import UUID

from app.models.timer import Timer, TimerStatus


class TimerRepository:
    """Repository for Timer persistence and retrieval."""

    def __init__(self, db_pool):
        """Initialize with asyncpg connection pool."""
        self.db_pool = db_pool

    async def create(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO timers (duration, elapsed_time, status, urgency_level, created_at, updated_at)
                VALUES ($1, $2, $3, $4, now(), now())
                RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
                """,
                duration,
                0,
                TimerStatus.IDLE.value,
                0,
            )
            return self._row_to_timer(row)

    async def get_by_id(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch timer by ID."""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at FROM timers WHERE id = $1",
                timer_id,
            )
            return self._row_to_timer(row) if row else None

    async def get_all(self) -> list[Timer]:
        """Fetch all timers."""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at FROM timers ORDER BY created_at DESC"
            )
            return [self._row_to_timer(row) for row in rows]

    async def update(self, timer: Timer) -> Timer:
        """Update timer in database."""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                UPDATE timers
                SET duration = $1, elapsed_time = $2, status = $3, urgency_level = $4, updated_at = now()
                WHERE id = $5
                RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
                """,
                timer.duration,
                timer.elapsed_time,
                timer.status.value,
                timer.urgency_level,
                timer.id,
            )
            return self._row_to_timer(row)

    async def delete(self, timer_id: UUID) -> None:
        """Delete timer by ID."""
        async with self.db_pool.acquire() as conn:
            await conn.execute("DELETE FROM timers WHERE id = $1", timer_id)

    def _row_to_timer(self, row) -> Timer:
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
