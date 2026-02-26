from uuid import UUID

from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepo


class TimerService:
    """Orchestrates timer lifecycle and business logic."""

    def __init__(self, repo: TimerRepo) -> None:
        self._repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with given duration (seconds)."""
        return await self._repo.create(duration)

    async def start_timer(self, timer_id: UUID) -> Timer:
        """Start a timer (set status to running)."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        urgency = self.compute_urgency(timer.elapsed_time, timer.duration)
        return await self._repo.update(timer_id, timer.elapsed_time, TimerStatus.running, urgency)

    async def stop_timer(self, timer_id: UUID) -> Timer:
        """Pause a timer (set status to paused)."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        return await self._repo.update(timer_id, timer.elapsed_time, TimerStatus.paused, timer.urgency_level)

    async def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset elapsed_time to 0 and set status to idle."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        return await self._repo.update(timer_id, 0, TimerStatus.idle, 0)

    async def tick_timer(self, timer_id: UUID) -> Timer:
        """Increment elapsed_time by 1 second and compute urgency."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        new_elapsed = timer.elapsed_time + 1
        new_urgency = self.compute_urgency(new_elapsed, timer.duration)
        new_status = TimerStatus.complete if new_elapsed >= timer.duration else timer.status
        return await self._repo.update(timer_id, new_elapsed, new_status, new_urgency)

    async def list_timers(self) -> list[Timer]:
        """List all timers."""
        return await self._repo.list_all()

    def compute_urgency(self, elapsed_time: int, duration: int) -> int:
        """Compute urgency level: 0–33% = 0, 33–66% = 1, 66–90% = 2, 90%+ = 3."""
        if duration == 0:
            return 0
        ratio = elapsed_time / duration
        if ratio < 0.33:
            return 0
        if ratio < 0.66:
            return 1
        if ratio < 0.90:
            return 2
        return 3
