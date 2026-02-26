from datetime import datetime
from uuid import UUID
from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepository


class TimerService:
    """Service layer for timer business logic."""

    def __init__(self, repo: TimerRepository):
        """Initialize with timer repository."""
        self.repo = repo

    def _compute_urgency_level(self, elapsed_time: int, duration: int) -> int:
        """Compute urgency level from elapsed time ratio."""
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
            raise ValueError("duration must be a positive integer")
        now = datetime.utcnow()
        timer = Timer(
            id=None,
            duration=duration,
            elapsed_time=0,
            status=TimerStatus.IDLE,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        return await self.repo.create(timer)

    async def set_duration(self, timer_id: UUID, duration: int) -> Timer:
        """Set or update timer duration."""
        if duration <= 0:
            raise ValueError("duration must be a positive integer")
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.duration = duration
        timer.urgency_level = self._compute_urgency_level(timer.elapsed_time, duration)
        return await self.repo.update(timer)

    async def start_timer(self, timer_id: UUID) -> Timer:
        """Start countdown from current elapsed_time."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.status = TimerStatus.RUNNING
        return await self.repo.update(timer)

    async def stop_timer(self, timer_id: UUID) -> Timer:
        """Pause countdown at current elapsed_time."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.status = TimerStatus.PAUSED
        return await self.repo.update(timer)

    async def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset elapsed_time to 0."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.elapsed_time = 0
        timer.status = TimerStatus.IDLE
        timer.urgency_level = 0
        return await self.repo.update(timer)

    async def get_timer(self, timer_id: UUID) -> Timer | None:
        """Retrieve timer by ID."""
        return await self.repo.get_by_id(timer_id)

    async def list_timers(self) -> list[Timer]:
        """Retrieve all timers."""
        return await self.repo.list_all()

    async def tick_timer(self, timer_id: UUID) -> Timer:
        """Increment elapsed_time by 1 second and update urgency_level."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        if timer.status != TimerStatus.RUNNING:
            return timer
        timer.elapsed_time += 1
        if timer.elapsed_time >= timer.duration:
            timer.elapsed_time = timer.duration
            timer.status = TimerStatus.COMPLETE
        timer.urgency_level = self._compute_urgency_level(timer.elapsed_time, timer.duration)
        return await self.repo.update(timer)
