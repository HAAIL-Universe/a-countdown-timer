from datetime import datetime
from uuid import UUID, uuid4

from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepo


class TimerService:
    """Service for managing timer business logic."""

    def __init__(self, repo: TimerRepo):
        """Initialize with timer repository."""
        self.repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        if duration <= 0:
            raise ValueError("Duration must be a positive integer")
        
        timer = Timer(
            id=uuid4(),
            duration=duration,
            elapsed_time=0,
            status=TimerStatus.IDLE,
            urgency_level=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return await self.repo.create(timer)

    async def get_timer(self, timer_id: UUID) -> Timer:
        """Fetch a timer by ID."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        return timer

    async def list_timers(self) -> list[Timer]:
        """Fetch all timers."""
        return await self.repo.get_all()

    async def set_duration(self, timer_id: UUID, duration: int) -> Timer:
        """Set or update timer duration."""
        if duration <= 0:
            raise ValueError("Duration must be a positive integer")
        
        timer = await self.get_timer(timer_id)
        timer.duration = duration
        timer.updated_at = datetime.utcnow()
        return await self.repo.update(timer)

    async def start_timer(self, timer_id: UUID) -> Timer:
        """Start countdown from current elapsed_time."""
        timer = await self.get_timer(timer_id)
        if timer.status == TimerStatus.COMPLETE:
            raise ValueError("Cannot start a completed timer")
        
        timer.status = TimerStatus.RUNNING
        timer.updated_at = datetime.utcnow()
        return await self.repo.update(timer)

    async def stop_timer(self, timer_id: UUID) -> Timer:
        """Pause countdown at current elapsed_time."""
        timer = await self.get_timer(timer_id)
        timer.status = TimerStatus.PAUSED
        timer.updated_at = datetime.utcnow()
        return await self.repo.update(timer)

    async def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset elapsed_time to 0."""
        timer = await self.get_timer(timer_id)
        timer.elapsed_time = 0
        timer.status = TimerStatus.IDLE
        timer.urgency_level = 0
        timer.updated_at = datetime.utcnow()
        return await self.repo.update(timer)

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

    async def tick_timer(self, timer_id: UUID) -> Timer:
        """Increment elapsed_time by 1 second and update urgency level."""
        timer = await self.get_timer(timer_id)
        
        if timer.status != TimerStatus.RUNNING:
            return timer
        
        timer.elapsed_time += 1
        
        if timer.elapsed_time >= timer.duration:
            timer.elapsed_time = timer.duration
            timer.status = TimerStatus.COMPLETE
            timer.urgency_level = 3
        else:
            timer.urgency_level = self.compute_urgency_level(
                timer.elapsed_time, timer.duration
            )
        
        timer.updated_at = datetime.utcnow()
        return await self.repo.update(timer)
