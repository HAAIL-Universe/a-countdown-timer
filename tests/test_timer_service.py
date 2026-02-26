import pytest
from datetime import datetime
from uuid import uuid4

from app.models.timer import Timer, TimerStatus
from app.services.timer_service import TimerService


class MockTimerRepo:
    """Mock repository for testing."""

    def __init__(self):
        self.timers: dict = {}

    async def create(self, timer: Timer) -> Timer:
        """Create a timer."""
        self.timers[timer.id] = timer
        return timer

    async def get_by_id(self, timer_id) -> Timer | None:
        """Get timer by ID."""
        return self.timers.get(timer_id)

    async def get_all(self) -> list[Timer]:
        """Get all timers."""
        return list(self.timers.values())

    async def update(self, timer: Timer) -> Timer:
        """Update a timer."""
        self.timers[timer.id] = timer
        return timer

    async def delete(self, timer_id) -> None:
        """Delete a timer."""
        if timer_id in self.timers:
            del self.timers[timer_id]


@pytest.fixture
def mock_repo():
    """Provide mock repository."""
    return MockTimerRepo()


@pytest.fixture
def service(mock_repo):
    """Provide timer service with mock repo."""
    return TimerService(mock_repo)


@pytest.mark.asyncio
async def test_create_timer(service):
    """Test creating a timer with valid duration."""
    timer = await service.create_timer(60)
    assert timer.duration == 60
    assert timer.elapsed_time == 0
    assert timer.status == TimerStatus.IDLE
    assert timer.urgency_level == 0


@pytest.mark.asyncio
async def test_create_timer_invalid_duration(service):
    """Test creating a timer with invalid duration."""
    with pytest.raises(ValueError):
        await service.create_timer(0)
    
    with pytest.raises(ValueError):
        await service.create_timer(-10)


@pytest.mark.asyncio
async def test_get_timer(service):
    """Test fetching a timer by ID."""
    created = await service.create_timer(60)
    fetched = await service.get_timer(created.id)
    assert fetched.id == created.id
    assert fetched.duration == 60


@pytest.mark.asyncio
async def test_get_timer_not_found(service):
    """Test fetching non-existent timer."""
    fake_id = uuid4()
    with pytest.raises(ValueError):
        await service.get_timer(fake_id)


@pytest.mark.asyncio
async def test_list_timers(service):
    """Test listing all timers."""
    await service.create_timer(60)
    await service.create_timer(120)
    timers = await service.list_timers()
    assert len(timers) == 2


@pytest.mark.asyncio
async def test_set_duration(service):
    """Test setting timer duration."""
    timer = await service.create_timer(60)
    updated = await service.set_duration(timer.id, 120)
    assert updated.duration == 120


@pytest.mark.asyncio
async def test_set_duration_invalid(service):
    """Test setting invalid duration."""
    timer = await service.create_timer(60)
    with pytest.raises(ValueError):
        await service.set_duration(timer.id, 0)


@pytest.mark.asyncio
async def test_start_timer(service):
    """Test starting a timer."""
    timer = await service.create_timer(60)
    started = await service.start_timer(timer.id)
    assert started.status == TimerStatus.RUNNING


@pytest.mark.asyncio
async def test_stop_timer(service):
    """Test pausing a timer."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    stopped = await service.stop_timer(timer.id)
    assert stopped.status == TimerStatus.PAUSED


@pytest.mark.asyncio
async def test_reset_timer(service):
    """Test resetting a timer."""
    timer = await service.create_timer(60)
    timer.elapsed_time = 30
    timer.status = TimerStatus.RUNNING
    await service.repo.update(timer)
    
    reset = await service.reset_timer(timer.id)
    assert reset.elapsed_time == 0
    assert reset.status == TimerStatus.IDLE
    assert reset.urgency_level == 0


@pytest.mark.asyncio
async def test_compute_urgency_level():
    """Test urgency level computation."""
    service = TimerService(MockTimerRepo())
    
    assert service.compute_urgency_level(0, 100) == 0
    assert service.compute_urgency_level(20, 100) == 0
    assert service.compute_urgency_level(33, 100) == 1
    assert service.compute_urgency_level(50, 100) == 1
    assert service.compute_urgency_level(66, 100) == 2
    assert service.compute_urgency_level(80, 100) == 2
    assert service.compute_urgency_level(90, 100) == 3
    assert service.compute_urgency_level(100, 100) == 3


@pytest.mark.asyncio
async def test_tick_timer_running(service):
    """Test incrementing elapsed time on running timer."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    
    ticked = await service.tick_timer(timer.id)
    assert ticked.elapsed_time == 1
    assert ticked.status == TimerStatus.RUNNING


@pytest.mark.asyncio
async def test_tick_timer_complete(service):
    """Test timer completion on tick."""
    timer = await service.create_timer(2)
    await service.start_timer(timer.id)
    await service.tick_timer(timer.id)
    
    completed = await service.tick_timer(timer.id)
    assert completed.elapsed_time == 2
    assert completed.status == TimerStatus.COMPLETE
    assert completed.urgency_level == 3


@pytest.mark.asyncio
async def test_tick_timer_paused(service):
    """Test ticking a paused timer does nothing."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    await service.tick_timer(timer.id)
    await service.stop_timer(timer.id)
    
    before_elapsed = timer.elapsed_time
    ticked = await service.tick_timer(timer.id)
    assert ticked.elapsed_time == before_elapsed


@pytest.mark.asyncio
async def test_tick_timer_updates_urgency_level(service):
    """Test urgency level updates on tick."""
    timer = await service.create_timer(100)
    await service.start_timer(timer.id)
    
    for _ in range(35):
        await service.tick_timer(timer.id)
    
    timer = await service.get_timer(timer.id)
    assert timer.urgency_level == 1
