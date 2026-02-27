from uuid import UUID
from app.repos.timer_repo import TimerRepo
from app.models.timer import Timer, TimerStatus


class TimerService:
    """Orchestrates timer lifecycle: create, start, stop, reset, tick; computes urgency."""

    def __init__(self, repo: TimerRepo) -> None:
        self._repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with given duration in seconds."""
        return await self._repo.create(duration)

    async def start_timer(self, timer_id: UUID) -> Timer:
        """Start a timer (change status to running)."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        urgency = self.compute_urgency(timer.elapsed_time, timer.duration)
        return await self._repo.update(timer_id, timer.elapsed_time, TimerStatus.running, urgency)

    async def stop_timer(self, timer_id: UUID) -> Timer:
        """Stop a timer (change status to paused)."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        urgency = self.compute_urgency(timer.elapsed_time, timer.duration)
        return await self._repo.update(timer_id, timer.elapsed_time, TimerStatus.paused, urgency)

    async def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset a timer to elapsed_time=0 and status=idle."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        return await self._repo.update(timer_id, 0, TimerStatus.idle, 0)

    async def tick_timer(self, timer_id: UUID) -> Timer:
        """Increment elapsed_time by 1 second and recompute urgency."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        new_elapsed = min(timer.elapsed_time + 1, timer.duration)
        status = TimerStatus.complete if new_elapsed >= timer.duration else timer.status
        urgency = self.compute_urgency(new_elapsed, timer.duration)
        return await self._repo.update(timer_id, new_elapsed, status, urgency)

    async def list_timers(self) -> list[Timer]:
        """List all timers."""
        return await self._repo.list_all()

    def compute_urgency(self, elapsed_time: int, duration: int) -> int:
        """Compute urgency level from elapsed_time / duration ratio.
        
        Returns:
            0 for 0–33% elapsed
            1 for 33–66% elapsed
            2 for 66–90% elapsed
            3 for 90%+ elapsed
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
