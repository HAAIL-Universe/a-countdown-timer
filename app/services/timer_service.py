from datetime import datetime
from uuid import UUID
from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepository


class TimerService:
    """Orchestrates timer business logic."""

    def __init__(self, repo: TimerRepository):
        """Initialize with timer repository."""
        self.repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        if duration <= 0:
            raise ValueError("Duration must be positive")
        return await self.repo.create(duration)

    async def get_timer(self, timer_id: UUID) -> Timer:
        """Fetch timer by ID."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        return timer

    async def get_all_timers(self) -> list[Timer]:
        """Fetch all timers."""
        return await self.repo.get_all()

    async def set_duration(self, timer_id: UUID, duration: int) -> Timer:
        """Update timer duration."""
        if duration <= 0:
            raise ValueError("Duration must be positive")
        timer = await self.get_timer(timer_id)
        return await self.repo.update(timer_id, duration=duration)

    async def start_timer(self, timer_id: UUID) -> Timer:
        """Start timer countdown."""
        timer = await self.get_timer(timer_id)
        if timer.status == TimerStatus.running:
            raise ValueError("Timer already running")
        return await self.repo.update(timer_id, status=TimerStatus.running)

    async def stop_timer(self, timer_id: UUID) -> Timer:
        """Pause timer countdown."""
        timer = await self.get_timer(timer_id)
        if timer.status != TimerStatus.running:
            raise ValueError("Timer is not running")
        return await self.repo.update(timer_id, status=TimerStatus.paused)

    async def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset elapsed_time to 0."""
        await self.get_timer(timer_id)
        return await self.repo.update(timer_id, elapsed_time=0, status=TimerStatus.idle)

    async def tick_timer(self, timer_id: UUID) -> Timer:
        """Increment elapsed_time by 1 second and update urgency."""
        timer = await self.get_timer(timer_id)
        if timer.status != TimerStatus.running:
            return timer

        new_elapsed = timer.elapsed_time + 1
        new_status = TimerStatus.running
        if new_elapsed >= timer.duration:
            new_elapsed = timer.duration
            new_status = TimerStatus.complete

        urgency = timer.calculate_urgency_level()
        return await self.repo.update(
            timer_id,
            elapsed_time=new_elapsed,
            status=new_status,
            urgency_level=urgency,
        )
