from typing import Optional
from uuid import UUID

import asyncpg

from app.models.timer import Timer, TimerStatus


class TimerRepository:
    """CRUD operations for timers using asyncpg."""

    def __init__(self, pool: asyncpg.Pool):
        """Initialize with asyncpg connection pool."""
        self.pool = pool

    async def create(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO timers (duration, elapsed_time, status, urgency_level)
                VALUES ($1, $2, $3, $4)
                RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
                """,
                duration,
                0,
                TimerStatus.IDLE.value,
                0,
            )
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=TimerStatus(row["status"]),
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def get_by_id(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch timer by ID."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
                FROM timers
                WHERE id = $1
                """,
                timer_id,
            )
        if not row:
            return None
        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=TimerStatus(row["status"]),
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def update(
        self,
        timer_id: UUID,
        elapsed_time: Optional[int] = None,
        status: Optional[TimerStatus] = None,
        urgency_level: Optional[int] = None,
    ) -> Optional[Timer]:
        """Update timer fields and return updated row."""
        updates = []
        params = [timer_id]
        param_idx = 2

        if elapsed_time is not None:
            updates.append(f"elapsed_time = ${param_idx}")
            params.append(elapsed_time)
            param_idx += 1

        if status is not None:
            updates.append(f"status = ${param_idx}")
            params.append(status.value)
            param_idx += 1

        if urgency_level is not None:
            updates.append(f"urgency_level = ${param_idx}")
            params.append(urgency_level)
            param_idx += 1

        if not updates:
            return await self.get_by_id(timer_id)

        updates.append("updated_at = NOW()")

        query = f"""
        UPDATE timers
        SET {', '.join(updates)}
        WHERE id = $1
        RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *params)

        if not row:
            return None

        return Timer(
            id=row["id"],
            duration=row["duration"],
            elapsed_time=row["elapsed_time"],
            status=TimerStatus(row["status"]),
            urgency_level=row["urgency_level"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
