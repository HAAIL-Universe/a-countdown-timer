from uuid import UUID

from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepo


class TimerService:
    """Orchestrates timer lifecycle: create, start, stop, reset, tick, and urgency computation."""

    def __init__(self, repo: TimerRepo) -> None:
        self.repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        if duration <= 0:
            raise ValueError("Duration must be positive")
        return await self.repo.create(duration)

    async def start_timer(self, timer_id: UUID) -> Timer:
        """Start countdown from current elapsed_time."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        if timer.status == TimerStatus.complete:
            raise ValueError("Cannot start a completed timer")
        
        timer = await self.repo.update(timer_id, timer.elapsed_time, TimerStatus.running, timer.urgency_level)
        return timer

    async def stop_timer(self, timer_id: UUID) -> Timer:
        """Pause countdown at current elapsed_time."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        timer = await self.repo.update(timer_id, timer.elapsed_time, TimerStatus.paused, timer.urgency_level)
        return timer

    async def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset elapsed_time to 0 and return to idle."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        timer = await self.repo.update(timer_id, 0, TimerStatus.idle, 0)
        return timer

    async def tick_timer(self, timer_id: UUID) -> Timer:
        """Increment elapsed_time by 1 second and update urgency level."""
        timer = await self.repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        if timer.status != TimerStatus.running:
            return timer
        
        new_elapsed = timer.elapsed_time + 1
        if new_elapsed >= timer.duration:
            new_elapsed = timer.duration
            new_status = TimerStatus.complete
            new_urgency = 3
        else:
            new_status = TimerStatus.running
            new_urgency = self.compute_urgency(new_elapsed, timer.duration)
        
        timer = await self.repo.update(timer_id, new_elapsed, new_status, new_urgency)
        return timer

    async def list_timers(self) -> list[Timer]:
        """Fetch all timers."""
        return await self.repo.list_all()

    def compute_urgency(self, elapsed_time: int, duration: int) -> int:
        """Compute urgency level (0-3) from elapsed_time / duration ratio.
        
        0: 0-33% elapsed
        1: 33-66% elapsed
        2: 66-90% elapsed
        3: 90%+ elapsed
        """
        if duration <= 0:
            return 0
        
        ratio = elapsed_time / duration
        if ratio < 0.33:
            return 0
        elif ratio < 0.66:
            return 1
        elif ratio < 0.90:
            return 2
        else:
            return 3
