from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

import asyncpg

from app.models.timer import Timer, TimerStatus


class TimerRepo:
    """Data access layer for timers table."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create(self, duration: int) -> Timer:
        """Insert a new timer and return it."""
        timer_id = uuid4()
        now = datetime.utcnow()
        query = """
            INSERT INTO timers (id, duration, elapsed_time, status, urgency_level, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                timer_id,
                duration,
                0,
                TimerStatus.idle.value,
                0,
                now,
                now,
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

    async def get_by_id(self, timer_id: UUID) -> Timer | None:
        """Fetch a timer by ID."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            WHERE id = $1
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, timer_id)
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

    async def list_all(self) -> list[Timer]:
        """Fetch all timers."""
        query = """
            SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at
            FROM timers
            ORDER BY created_at DESC
        """
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [
            Timer(
                id=row["id"],
                duration=row["duration"],
                elapsed_time=row["elapsed_time"],
                status=TimerStatus(row["status"]),
                urgency_level=row["urgency_level"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

    async def update(
        self, timer_id: UUID, elapsed_time: int, status: TimerStatus, urgency_level: int
    ) -> Timer | None:
        """Update a timer's elapsed_time, status, and urgency_level."""
        now = datetime.utcnow()
        query = """
            UPDATE timers
            SET elapsed_time = $2, status = $3, urgency_level = $4, updated_at = $5
            WHERE id = $1
            RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
        """
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                query, timer_id, elapsed_time, status.value, urgency_level, now
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
