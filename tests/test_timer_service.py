import pytest
from datetime import datetime
from uuid import uuid4
from app.services.timer_service import TimerService
from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepository


class MockTimerRepository(TimerRepository):
    """Mock repository for testing."""

    def __init__(self):
        """Initialize mock repository with in-memory storage."""
        self.timers = {}

    async def create(self, duration: int) -> Timer:
        """Create a new timer."""
        timer = Timer(
            id=uuid4(),
            duration=duration,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.timers[timer.id] = timer
        return timer

    async def get_by_id(self, timer_id) -> Timer | None:
        """Fetch timer by ID."""
        return self.timers.get(timer_id)

    async def get_all(self) -> list[Timer]:
        """Fetch all timers."""
        return list(self.timers.values())

    async def update(self, timer_id, **kwargs) -> Timer:
        """Update timer with given fields."""
        timer = self.timers.get(timer_id)
        if not timer:
            return None
        for key, value in kwargs.items():
            if hasattr(timer, key):
                setattr(timer, key, value)
        timer.updated_at = datetime.now()
        self.timers[timer_id] = timer
        return timer


@pytest.fixture
def mock_repo():
    """Provide mock repository."""
    return MockTimerRepository()


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
    assert timer.status == TimerStatus.idle
    assert timer.urgency_level == 0


@pytest.mark.asyncio
async def test_create_timer_invalid_duration(service):
    """Test creating timer with invalid duration raises error."""
    with pytest.raises(ValueError, match="Duration must be positive"):
        await service.create_timer(0)
    with pytest.raises(ValueError, match="Duration must be positive"):
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
    """Test fetching non-existent timer raises error."""
    fake_id = uuid4()
    with pytest.raises(ValueError, match="not found"):
        await service.get_timer(fake_id)


@pytest.mark.asyncio
async def test_get_all_timers(service):
    """Test fetching all timers."""
    await service.create_timer(60)
    await service.create_timer(120)
    timers = await service.get_all_timers()
    assert len(timers) == 2


@pytest.mark.asyncio
async def test_set_duration(service):
    """Test updating timer duration."""
    timer = await service.create_timer(60)
    updated = await service.set_duration(timer.id, 120)
    assert updated.duration == 120


@pytest.mark.asyncio
async def test_set_duration_invalid(service):
    """Test setting invalid duration raises error."""
    timer = await service.create_timer(60)
    with pytest.raises(ValueError, match="Duration must be positive"):
        await service.set_duration(timer.id, 0)


@pytest.mark.asyncio
async def test_start_timer(service):
    """Test starting a timer."""
    timer = await service.create_timer(60)
    started = await service.start_timer(timer.id)
    assert started.status == TimerStatus.running


@pytest.mark.asyncio
async def test_start_timer_already_running(service):
    """Test starting an already running timer raises error."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    with pytest.raises(ValueError, match="already running"):
        await service.start_timer(timer.id)


@pytest.mark.asyncio
async def test_stop_timer(service):
    """Test pausing a running timer."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    stopped = await service.stop_timer(timer.id)
    assert stopped.status == TimerStatus.paused


@pytest.mark.asyncio
async def test_stop_timer_not_running(service):
    """Test stopping a non-running timer raises error."""
    timer = await service.create_timer(60)
    with pytest.raises(ValueError, match="not running"):
        await service.stop_timer(timer.id)


@pytest.mark.asyncio
async def test_reset_timer(service):
    """Test resetting timer elapsed time."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    reset = await service.reset_timer(timer.id)
    assert reset.elapsed_time == 0
    assert reset.status == TimerStatus.idle


@pytest.mark.asyncio
async def test_tick_timer(service):
    """Test timer tick increments elapsed time."""
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    ticked = await service.tick_timer(timer.id)
    assert ticked.elapsed_time == 1
    assert ticked.status == TimerStatus.running


@pytest.mark.asyncio
async def test_tick_timer_reaches_duration(service):
    """Test timer tick completes when elapsed reaches duration."""
    timer = await service.create_timer(5)
    await service.start_timer(timer.id)
    for _ in range(5):
        ticked = await service.tick_timer(timer.id)
    assert ticked.elapsed_time == 5
    assert ticked.status == TimerStatus.complete


@pytest.mark.asyncio
async def test_tick_timer_not_running(service):
    """Test tick on paused timer does not increment."""
    timer = await service.create_timer(60)
    ticked = await service.tick_timer(timer.id)
    assert ticked.elapsed_time == 0


@pytest.mark.asyncio
async def test_urgency_level_calculation(service):
    """Test urgency level updates with elapsed time."""
    timer = await service.create_timer(100)
    await service.start_timer(timer.id)

    for _ in range(20):
        await service.tick_timer(timer.id)
    timer = await service.get_timer(timer.id)
    assert timer.urgency_level == 0

    for _ in range(20):
        await service.tick_timer(timer.id)
    timer = await service.get_timer(timer.id)
    assert timer.urgency_level == 1

    for _ in range(20):
        await service.tick_timer(timer.id)
    timer = await service.get_timer(timer.id)
    assert timer.urgency_level == 2

    for _ in range(20):
        await service.tick_timer(timer.id)
    timer = await service.get_timer(timer.id)
    assert timer.urgency_level == 3
