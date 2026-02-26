from uuid import UUID
from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepo


class TimerService:
    """Orchestrates timer lifecycle and business logic."""

    def __init__(self, repo: TimerRepo) -> None:
        self._repo = repo

    async def create_timer(self, duration: int) -> Timer:
        """Create a new timer with the specified duration in seconds."""
        return await self._repo.create(duration)

    async def start_timer(self, timer_id: UUID) -> Timer:
        """Transition timer to running status."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        if timer.status in (TimerStatus.idle, TimerStatus.paused):
            urgency = self.compute_urgency(timer.elapsed_time, timer.duration)
            return await self._repo.update(
                timer_id,
                elapsed_time=timer.elapsed_time,
                status=TimerStatus.running,
                urgency_level=urgency,
            )
        return timer

    async def stop_timer(self, timer_id: UUID) -> Timer:
        """Pause the running timer."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        if timer.status == TimerStatus.running:
            urgency = self.compute_urgency(timer.elapsed_time, timer.duration)
            return await self._repo.update(
                timer_id,
                elapsed_time=timer.elapsed_time,
                status=TimerStatus.paused,
                urgency_level=urgency,
            )
        return timer

    async def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset timer to idle status with zero elapsed time."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        return await self._repo.update(
            timer_id,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
        )

    async def tick_timer(self, timer_id: UUID) -> Timer:
        """Increment elapsed_time by 1 second and update urgency. Transition to complete if elapsed >= duration."""
        timer = await self._repo.get_by_id(timer_id)
        if timer is None:
            return None
        if timer.status != TimerStatus.running:
            return timer
        new_elapsed = timer.elapsed_time + 1
        new_status = TimerStatus.complete if new_elapsed >= timer.duration else TimerStatus.running
        urgency = self.compute_urgency(new_elapsed, timer.duration)
        return await self._repo.update(
            timer_id,
            elapsed_time=new_elapsed,
            status=new_status,
            urgency_level=urgency,
        )

    async def list_timers(self) -> list[Timer]:
        """List all timers."""
        return await self._repo.list_all()

    def compute_urgency(self, elapsed_time: int, duration: int) -> int:
        """Compute urgency level (0–3) based on percentage of duration elapsed."""
        if duration <= 0:
            return 0
        percentage = (elapsed_time / duration) * 100
        if percentage < 33:
            return 0
        elif percentage < 66:
            return 1
        elif percentage < 90:
            return 2
        else:
            return 3
