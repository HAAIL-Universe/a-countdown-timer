from uuid import UUID

from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepo


class TimerService:
    """Business logic for timer operations."""

    def __init__(self, repo: TimerRepo) -> None:
        self._repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with given duration."""
        return await self._repo.create(duration)

    async def start_timer(self, timer_id: UUID) -> Timer:
        """Start a timer. Timer must be idle or paused."""
        timer = await self._repo.get_by_id(timer_id)
        if not timer:
            return None
        if timer.status not in (TimerStatus.idle, TimerStatus.paused):
            return timer
        urgency = self.compute_urgency(timer.elapsed_time, timer.duration)
        return await self._repo.update(timer_id, timer.elapsed_time, TimerStatus.running, urgency)

    async def stop_timer(self, timer_id: UUID) -> Timer:
        """Pause a running timer."""
        timer = await self._repo.get_by_id(timer_id)
        if not timer:
            return None
        if timer.status != TimerStatus.running:
            return timer
        urgency = self.compute_urgency(timer.elapsed_time, timer.duration)
        return await self._repo.update(timer_id, timer.elapsed_time, TimerStatus.paused, urgency)

    async def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset timer elapsed time to zero."""
        timer = await self._repo.get_by_id(timer_id)
        if not timer:
            return None
        urgency = self.compute_urgency(0, timer.duration)
        return await self._repo.update(timer_id, 0, TimerStatus.idle, urgency)

    async def tick_timer(self, timer_id: UUID) -> Timer:
        """Increment elapsed_time by one second. Mark complete if elapsed >= duration."""
        timer = await self._repo.get_by_id(timer_id)
        if not timer:
            return None
        if timer.status != TimerStatus.running:
            return timer
        new_elapsed = timer.elapsed_time + 1
        new_status = TimerStatus.complete if new_elapsed >= timer.duration else TimerStatus.running
        urgency = self.compute_urgency(new_elapsed, timer.duration)
        return await self._repo.update(timer_id, new_elapsed, new_status, urgency)

    async def list_timers(self) -> list[Timer]:
        """Fetch all timers."""
        return await self._repo.list_all()

    def compute_urgency(self, elapsed_time: int, duration: int) -> int:
        """Compute urgency level 0-3 based on elapsed_time / duration ratio."""
        if duration == 0:
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
