from uuid import UUID
from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepo


class TimerService:
    """Orchestrates timer operations and computes urgency level."""

    def __init__(self, repo: TimerRepo) -> None:
        self._repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with the given duration."""
        if duration <= 0:
            raise ValueError("Duration must be a positive integer")
        return await self._repo.create(duration)

    async def get_timer(self, timer_id: UUID) -> Timer:
        """Fetch a timer by ID; raise if not found."""
        timer = await self._repo.get_by_id(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        return timer

    async def list_timers(self) -> list[Timer]:
        """List all timers."""
        return await self._repo.list_all()

    async def set_duration(self, timer_id: UUID, duration: int) -> Timer:
        """Set or update the timer's duration."""
        if duration <= 0:
            raise ValueError("Duration must be a positive integer")
        timer = await self.get_timer(timer_id)
        urgency = self._compute_urgency_level(0, duration)
        return await self._repo.update(
            timer_id,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=urgency,
        ) or timer

    async def start_timer(self, timer_id: UUID) -> Timer:
        """Start the countdown from current elapsed_time."""
        timer = await self.get_timer(timer_id)
        if timer.elapsed_time >= timer.duration:
            raise ValueError("Timer has already completed")
        urgency = self._compute_urgency_level(timer.elapsed_time, timer.duration)
        return await self._repo.update(
            timer_id,
            elapsed_time=timer.elapsed_time,
            status=TimerStatus.running,
            urgency_level=urgency,
        ) or timer

    async def stop_timer(self, timer_id: UUID) -> Timer:
        """Pause the countdown at current elapsed_time."""
        timer = await self.get_timer(timer_id)
        urgency = self._compute_urgency_level(timer.elapsed_time, timer.duration)
        return await self._repo.update(
            timer_id,
            elapsed_time=timer.elapsed_time,
            status=TimerStatus.paused,
            urgency_level=urgency,
        ) or timer

    async def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset elapsed_time to 0 and return to idle status."""
        timer = await self.get_timer(timer_id)
        return await self._repo.update(
            timer_id,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
        ) or timer

    async def tick_timer(self, timer_id: UUID) -> Timer:
        """Increment elapsed_time by 1 second and update urgency; mark complete if reached duration."""
        timer = await self.get_timer(timer_id)
        if timer.status != TimerStatus.running:
            return timer
        new_elapsed = min(timer.elapsed_time + 1, timer.duration)
        new_status = TimerStatus.complete if new_elapsed >= timer.duration else TimerStatus.running
        urgency = self._compute_urgency_level(new_elapsed, timer.duration)
        return await self._repo.update(
            timer_id,
            elapsed_time=new_elapsed,
            status=new_status,
            urgency_level=urgency,
        ) or timer

    @staticmethod
    def _compute_urgency_level(elapsed_time: int, duration: int) -> int:
        """Compute urgency level (0-3) based on elapsed_time / duration ratio."""
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
