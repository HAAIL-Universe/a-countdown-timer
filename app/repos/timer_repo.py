from uuid import UUID
from datetime import datetime
from typing import Optional, List
import asyncpg
from app.models.timer import Timer


class TimerRepository:
    """Repository for Timer persistence."""

    def __init__(self, pool: asyncpg.Pool):
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
        """Fetch a timer by ID."""
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

    async def update(self, timer_id: UUID, **kwargs) -> Optional[Timer]:
        """Update timer fields and return updated record."""
        allowed_fields = {
            "duration",
            "elapsed_time",
            "status",
            "urgency_level",
        }
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return await self.get_by_id(timer_id)

        updates["updated_at"] = datetime.utcnow()
        set_clause = ", ".join([f"{k} = ${i+1}" for i, k in enumerate(updates.keys())])
        values = list(updates.values())

        query = f"""
            UPDATE timers
            SET {set_clause}
            WHERE id = ${len(values) + 1}
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        row = await self.pool.fetchrow(query, *values, timer_id)
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
        """Delete a timer by ID."""
        query = "DELETE FROM timers WHERE id = $1"
        result = await self.pool.execute(query, timer_id)
        return result == "DELETE 1"
