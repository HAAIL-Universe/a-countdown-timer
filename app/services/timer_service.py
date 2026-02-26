from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.timer import Timer
from app.repos.timer_repository import TimerRepository


class TimerService:
    """Service for timer operations and business logic."""

    def __init__(self, repo: TimerRepository) -> None:
        """Initialize timer service with repository."""
        self.repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with given duration in seconds."""
        if duration <= 0:
            raise ValueError("Duration must be a positive integer")
        
        timer = Timer(
            id=None,
            duration=duration,
            elapsed_time=0,
            status="idle",
            urgency_level=0,
            created_at=None,
            updated_at=None,
        )
        return await self.repo.create(timer)

    async def get_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch a timer by ID."""
        return await self.repo.get(timer_id)

    async def list_timers(self) -> list[Timer]:
        """List all timers."""
        return await self.repo.list_all()

    async def set_duration(self, timer_id: UUID, duration: int) -> Timer:
        """Update timer duration."""
        if duration <= 0:
            raise ValueError("Duration must be a positive integer")
        
        timer = await self.repo.get(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        timer.duration = duration
        timer.updated_at = datetime.utcnow()
        return await self.repo.update(timer)

    async def start_timer(self, timer_id: UUID) -> Timer:
        """Start a timer countdown."""
        timer = await self.repo.get(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        timer.status = "running"
        timer.updated_at = datetime.utcnow()
        return await self.repo.update(timer)

    async def stop_timer(self, timer_id: UUID) -> Timer:
        """Pause a running timer."""
        timer = await self.repo.get(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        timer.status = "paused"
        timer.updated_at = datetime.utcnow()
        return await self.repo.update(timer)

    async def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset elapsed_time to 0."""
        timer = await self.repo.get(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        timer.elapsed_time = 0
        timer.status = "idle"
        timer.urgency_level = 0
        timer.updated_at = datetime.utcnow()
        return await self.repo.update(timer)

    def compute_urgency_level(self, elapsed_time: int, duration: int) -> int:
        """Compute urgency level (0–3) from elapsed_time ratio."""
        if duration == 0:
            return 0
        
        ratio = elapsed_time / duration
        
        if ratio >= 0.9:
            return 3
        elif ratio >= 0.66:
            return 2
        elif ratio >= 0.33:
            return 1
        else:
            return 0

    async def tick_timer(self, timer_id: UUID) -> Timer:
        """Increment elapsed_time by 1 second and update urgency level."""
        timer = await self.repo.get(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        if timer.status != "running":
            return timer
        
        timer.elapsed_time += 1
        timer.urgency_level = self.compute_urgency_level(
            timer.elapsed_time, timer.duration
        )
        
        if timer.elapsed_time >= timer.duration:
            timer.elapsed_time = timer.duration
            timer.status = "complete"
        
        timer.updated_at = datetime.utcnow()
        return await self.repo.update(timer)
