from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepository


class TimerService:
    """Service for timer business logic and state management."""

    def __init__(self, repo: TimerRepository):
        """Initialize service with timer repository."""
        self.repo = repo

    def _compute_urgency_level(self, elapsed_time: int, duration: int) -> int:
        """Compute urgency level based on elapsed time ratio."""
        if duration <= 0:
            return 0
        ratio = elapsed_time / duration
        if ratio < 0.33:
            return 0
        elif ratio < 0.66:
            return 1
        elif ratio < 0.9:
            return 2
        else:
            return 3

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        if duration <= 0:
            raise ValueError("Duration must be positive")

        result = await self.repo.create(
            duration=duration,
            elapsed_time=0,
            status=TimerStatus.IDLE.value,
            urgency_level=0,
        )

        return self._dict_to_timer(result)

    async def get_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch a timer by ID."""
        result = await self.repo.get_by_id(timer_id)
        return self._dict_to_timer(result) if result else None

    async def list_timers(self) -> list[Timer]:
        """Fetch all timers."""
        results = await self.repo.list_all()
        return [self._dict_to_timer(r) for r in results]

    async def set_duration(self, timer_id: UUID, duration: int) -> Optional[Timer]:
        """Set or update timer duration."""
        if duration <= 0:
            raise ValueError("Duration must be positive")

        result = await self.repo.update(timer_id=timer_id, duration=duration)
        return self._dict_to_timer(result) if result else None

    async def start_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Start timer countdown."""
        timer = await self.get_timer(timer_id)
        if not timer:
            return None

        result = await self.repo.update(
            timer_id=timer_id,
            status=TimerStatus.RUNNING.value,
        )
        return self._dict_to_timer(result) if result else None

    async def stop_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Pause timer countdown."""
        timer = await self.get_timer(timer_id)
        if not timer:
            return None

        result = await self.repo.update(
            timer_id=timer_id,
            status=TimerStatus.PAUSED.value,
        )
        return self._dict_to_timer(result) if result else None

    async def reset_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Reset elapsed time to 0."""
        timer = await self.get_timer(timer_id)
        if not timer:
            return None

        result = await self.repo.update(
            timer_id=timer_id,
            elapsed_time=0,
            status=TimerStatus.IDLE.value,
            urgency_level=0,
        )
        return self._dict_to_timer(result) if result else None

    def _dict_to_timer(self, data: Optional[dict]) -> Optional[Timer]:
        """Convert repository dict to Timer model."""
        if not data:
            return None

        return Timer(
            id=data["id"],
            duration=data["duration"],
            elapsed_time=data["elapsed_time"],
            status=TimerStatus(data["status"]),
            urgency_level=data["urgency_level"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
