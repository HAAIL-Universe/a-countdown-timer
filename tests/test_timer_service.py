import pytest
from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock

from app.models.timer import Timer, TimerStatus
from app.services.timer_service import TimerService


class MockTimerRepo:
    """Mock repository for testing TimerService."""

    def __init__(self):
        self.timers: dict = {}

    async def create(self, duration: int) -> Timer:
        """Create a timer with given duration."""
        timer_id = uuid4()
        now = datetime.utcnow()
        timer = Timer(
            id=timer_id,
            duration=duration,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        self.timers[timer_id] = timer
        return timer

    async def get_by_id(self, timer_id) -> Timer | None:
        """Get timer by ID."""
        return self.timers.get(timer_id)

    async def list_all(self) -> list[Timer]:
        """Get all timers."""
        return list(self.timers.values())

    async def update(
        self, timer_id, elapsed_time: int, status: TimerStatus, urgency_level: int
    ) -> Timer | None:
        """Update timer state."""
        timer = self.timers.get(timer_id)
        if not timer:
            return None
        now = datetime.utcnow()
        timer.elapsed_time = elapsed_time
        timer.status = status
        timer.urgency_level = urgency_level
        timer.updated_at = now
        self.timers[timer_id] = timer
        return timer

    async def delete(self, timer_id) -> bool:
        """Delete a timer."""
        if timer_id in self.timers:
            del self.timers[timer_id]
            return True
        return False


@pytest.fixture
def mock_repo():
    """Provide mock repository."""
    return MockTimerRepo()


@pytest.fixture
def service(mock_repo):
    """Provide timer service with mock repo."""
    return TimerService(mock_repo)


@pytest.mark.asyncio
async def test_create_timer_sets_idle_status(service):
    """AC-0-2: TimerRepo.create inserts a row with status=idle and elapsed_time=0 and returns a Timer with a valid UUID."""
    timer = await service.create_timer(60)

    assert timer.id is not None
    assert timer.duration == 60
    assert timer.elapsed_time == 0
    assert timer.status == TimerStatus.idle
    assert timer.urgency_level == 0
    assert timer.created_at is not None
    assert timer.updated_at is not None


@pytest.mark.asyncio
async def test_compute_urgency_levels(service):
    """AC-0-1: TimerService.compute_urgency returns correct levels for different elapsed ratios."""
    # Test 0-33% elapsed → level 0
    assert service.compute_urgency(0, 100) == 0
    assert service.compute_urgency(10, 100) == 0
    assert service.compute_urgency(32, 100) == 0

    # Test 33-66% elapsed → level 1
    assert service.compute_urgency(33, 100) == 1
    assert service.compute_urgency(50, 100) == 1
    assert service.compute_urgency(65, 100) == 1

    # Test 66-90% elapsed → level 2
    assert service.compute_urgency(66, 100) == 2
    assert service.compute_urgency(75, 100) == 2
    assert service.compute_urgency(89, 100) == 2

    # Test 90%+ elapsed → level 3
    assert service.compute_urgency(90, 100) == 3
    assert service.compute_urgency(99, 100) == 3
    assert service.compute_urgency(100, 100) == 3


@pytest.mark.asyncio
async def test_start_timer_sets_running_status(service):
    """Test that starting a timer sets status to running."""
    timer = await service.create_timer(60)

    started = await service.start_timer(timer.id)

    assert started.status == TimerStatus.running
    assert started.elapsed_time == 0


@pytest.mark.asyncio
async def test_stop_timer_sets_paused_status(service):
    """Test that stopping a timer sets status to paused."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)

    stopped = await service.stop_timer(timer.id)

    assert stopped.status == TimerStatus.paused
    assert stopped.elapsed_time == 0


@pytest.mark.asyncio
async def test_reset_timer_clears_elapsed_time(service):
    """Test that resetting a timer clears elapsed_time and returns to idle."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    await service.tick_timer(timer.id)

    reset = await service.reset_timer(timer.id)

    assert reset.elapsed_time == 0
    assert reset.status == TimerStatus.idle
    assert reset.urgency_level == 0


@pytest.mark.asyncio
async def test_create_timer_invalid_duration(service):
    """Test creating a timer with invalid duration raises ValueError."""
    with pytest.raises(ValueError):
        await service.create_timer(0)

    with pytest.raises(ValueError):
        await service.create_timer(-10)


@pytest.mark.asyncio
async def test_start_timer_not_found(service):
    """Test starting a non-existent timer raises ValueError."""
    fake_id = uuid4()
    with pytest.raises(ValueError):
        await service.start_timer(fake_id)


@pytest.mark.asyncio
async def test_start_completed_timer_raises_error(service):
    """Test that starting a completed timer raises ValueError."""
    timer = await service.create_timer(2)
    await service.start_timer(timer.id)

    # Tick twice to complete the timer
    await service.tick_timer(timer.id)
    await service.tick_timer(timer.id)

    with pytest.raises(ValueError):
        await service.start_timer(timer.id)


@pytest.mark.asyncio
async def test_tick_timer_increments_elapsed_time(service):
    """Test that ticking a running timer increments elapsed_time."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)

    ticked = await service.tick_timer(timer.id)

    assert ticked.elapsed_time == 1
    assert ticked.status == TimerStatus.running


@pytest.mark.asyncio
async def test_tick_timer_completes_on_duration_reached(service):
    """Test that timer completes when elapsed_time reaches duration."""
    timer = await service.create_timer(2)
    await service.start_timer(timer.id)

    await service.tick_timer(timer.id)
    completed = await service.tick_timer(timer.id)

    assert completed.elapsed_time == 2
    assert completed.status == TimerStatus.complete
    assert completed.urgency_level == 3


@pytest.mark.asyncio
async def test_tick_timer_paused_does_nothing(service):
    """Test that ticking a paused timer does not change elapsed_time."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    await service.tick_timer(timer.id)
    await service.stop_timer(timer.id)

    paused_elapsed = (await service.repo.get_by_id(timer.id)).elapsed_time
    ticked = await service.tick_timer(timer.id)

    assert ticked.elapsed_time == paused_elapsed


@pytest.mark.asyncio
async def test_tick_timer_updates_urgency_correctly(service):
    """Test that urgency_level updates correctly as timer ticks."""
    timer = await service.create_timer(100)
    await service.start_timer(timer.id)

    # Tick to ~50% (urgency level 1)
    for _ in range(50):
        await service.tick_timer(timer.id)

    updated = await service.repo.get_by_id(timer.id)
    assert updated.urgency_level == 1


@pytest.mark.asyncio
async def test_list_timers(service):
    """Test that list_timers returns all created timers."""
    timer1 = await service.create_timer(60)
    timer2 = await service.create_timer(120)

    timers = await service.list_timers()

    assert len(timers) == 2
    assert any(t.id == timer1.id for t in timers)
    assert any(t.id == timer2.id for t in timers)


@pytest.mark.asyncio
async def test_tick_timer_not_found(service):
    """Test ticking a non-existent timer raises ValueError."""
    fake_id = uuid4()
    with pytest.raises(ValueError):
        await service.tick_timer(fake_id)


@pytest.mark.asyncio
async def test_compute_urgency_edge_cases(service):
    """Test urgency computation with edge cases and boundary values."""
    # Duration of 1
    assert service.compute_urgency(0, 1) == 0
    assert service.compute_urgency(1, 1) == 3

    # Very large duration
    assert service.compute_urgency(0, 10000) == 0
    assert service.compute_urgency(3300, 10000) == 1
    assert service.compute_urgency(6600, 10000) == 2
    assert service.compute_urgency(9000, 10000) == 3

    # Boundary exactly at 33%
    assert service.compute_urgency(33, 100) == 1

    # Boundary exactly at 66%
    assert service.compute_urgency(66, 100) == 2

    # Boundary exactly at 90%
    assert service.compute_urgency(90, 100) == 3
