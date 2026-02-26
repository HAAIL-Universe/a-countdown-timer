from uuid import UUID

from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepo


class TimerService:
    """Orchestrates timer lifecycle and urgency computation."""

    def __init__(self, repo: TimerRepo) -> None:
        self._repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with the given duration."""
        return await self._repo.create(duration)

    async def start_timer(self, timer_id: UUID) -> Timer | None:
        """Set timer status to running."""
        timer = await self._repo.get_by_id(timer_id)
        if not timer:
            return None
        urgency = self.compute_urgency(timer.elapsed_time, timer.duration)
        return await self._repo.update(timer_id, timer.elapsed_time, TimerStatus.running, urgency)

    async def stop_timer(self, timer_id: UUID) -> Timer | None:
        """Set timer status to paused."""
        timer = await self._repo.get_by_id(timer_id)
        if not timer:
            return None
        urgency = self.compute_urgency(timer.elapsed_time, timer.duration)
        return await self._repo.update(timer_id, timer.elapsed_time, TimerStatus.paused, urgency)

    async def reset_timer(self, timer_id: UUID) -> Timer | None:
        """Reset timer elapsed_time to 0 and set status to idle."""
        timer = await self._repo.get_by_id(timer_id)
        if not timer:
            return None
        return await self._repo.update(timer_id, 0, TimerStatus.idle, 0)

    async def tick_timer(self, timer_id: UUID) -> Timer | None:
        """Increment elapsed_time by 1 second and update urgency."""
        timer = await self._repo.get_by_id(timer_id)
        if not timer:
            return None
        new_elapsed = timer.elapsed_time + 1
        urgency = self.compute_urgency(new_elapsed, timer.duration)
        status = TimerStatus.complete if new_elapsed >= timer.duration else timer.status
        return await self._repo.update(timer_id, new_elapsed, status, urgency)

    async def list_timers(self) -> list[Timer]:
        """Fetch all timers."""
        return await self._repo.list_all()

    def compute_urgency(self, elapsed_time: int, duration: int) -> int:
        """Return urgency level (0–3) based on elapsed_time / duration ratio."""
        if duration <= 0:
            return 0
        ratio = elapsed_time / duration
        if ratio < 0.33:
            return 0
        if ratio < 0.66:
            return 1
        if ratio < 0.90:
            return 2
        return 3
