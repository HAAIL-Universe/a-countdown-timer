from typing import Optional
from uuid import UUID

from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepository


class TimerService:
    """Orchestrate timer logic and state transitions."""

    def __init__(self, repo: TimerRepository) -> None:
        self.repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        if duration <= 0:
            raise ValueError("Duration must be a positive integer")
        return await self.repo.create(duration)

    async def set_duration(self, timer_id: UUID, duration: int) -> Timer:
        """Update timer duration."""
        if duration <= 0:
            raise ValueError("Duration must be a positive integer")
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.duration = duration
        return await self.repo.update(timer)

    async def start(self, timer_id: UUID) -> Timer:
        """Start countdown."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.status = TimerStatus.RUNNING
        return await self.repo.update(timer)

    async def stop(self, timer_id: UUID) -> Timer:
        """Pause countdown."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.status = TimerStatus.PAUSED
        return await self.repo.update(timer)

    async def reset(self, timer_id: UUID) -> Timer:
        """Reset elapsed_time to 0."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.elapsed_time = 0
        timer.status = TimerStatus.IDLE
        return await self.repo.update(timer)

    async def get_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch timer by ID."""
        return await self.repo.get_by_id(timer_id)

    async def list_timers(self) -> list[Timer]:
        """List all timers."""
        return await self.repo.list_all()

    def compute_urgency_level(self, elapsed_time: int, duration: int) -> int:
        """Compute urgency level (0-3) from elapsed_time / duration ratio."""
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

    def get_color(self, elapsed_time: int, duration: int) -> str:
        """Return color based on progress: green, yellow, or red."""
        if duration <= 0:
            return "green"
        ratio = elapsed_time / duration
        if ratio < 0.33:
            return "green"
        elif ratio < 0.66:
            return "yellow"
        else:
            return "red"
