import pytest
from uuid import uuid4
from datetime import datetime
from app.models.timer import Timer, TimerStatus
from app.services.timer_service import TimerService
from app.repos.timer_repo import TimerRepo


class MockTimerRepo(TimerRepo):
    """Mock timer repository for testing."""

    def __init__(self):
        self.timers = {}

    async def create(self, duration: int) -> Timer:
        """Create a new timer."""
        timer_id = uuid4()
        now = datetime.utcnow()
        timer = Timer(
            id=timer_id,
            duration=duration,
            elapsed_time=0,
            status=TimerStatus.IDLE,
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
        """List all timers."""
        return list(self.timers.values())

    async def update(
        self,
        timer_id,
        elapsed_time: int | None = None,
        status: TimerStatus | None = None,
        urgency_level: int | None = None,
    ) -> Timer | None:
        """Update timer fields."""
        timer = self.timers.get(timer_id)
        if not timer:
            return None
        now = datetime.utcnow()
        updated = Timer(
            id=timer.id,
            duration=timer.duration,
            elapsed_time=elapsed_time if elapsed_time is not None else timer.elapsed_time,
            status=status if status is not None else timer.status,
            urgency_level=urgency_level if urgency_level is not None else timer.urgency_level,
            created_at=timer.created_at,
            updated_at=now,
        )
        self.timers[timer_id] = updated
        return updated


@pytest.mark.asyncio
async def test_create_timer():
    """Test creating a timer with valid duration."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    assert timer.duration == 60
    assert timer.elapsed_time == 0
    assert timer.status == TimerStatus.IDLE
    assert timer.urgency_level == 0


@pytest.mark.asyncio
async def test_create_timer_invalid_duration():
    """Test creating a timer with invalid duration."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    with pytest.raises(ValueError, match="Duration must be a positive integer"):
        await service.create_timer(0)
    with pytest.raises(ValueError, match="Duration must be a positive integer"):
        await service.create_timer(-10)


@pytest.mark.asyncio
async def test_get_timer():
    """Test fetching a timer by ID."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    fetched = await service.get_timer(timer.id)
    assert fetched.id == timer.id
    assert fetched.duration == 60


@pytest.mark.asyncio
async def test_get_timer_not_found():
    """Test fetching a non-existent timer."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    with pytest.raises(ValueError, match="not found"):
        await service.get_timer(uuid4())


@pytest.mark.asyncio
async def test_list_timers():
    """Test listing all timers."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    await service.create_timer(60)
    await service.create_timer(120)
    timers = await service.list_timers()
    assert len(timers) == 2


@pytest.mark.asyncio
async def test_set_duration():
    """Test setting timer duration."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    updated = await service.set_duration(timer.id, 120)
    assert updated.duration == 120
    assert updated.elapsed_time == 0
    assert updated.status == TimerStatus.IDLE
    assert updated.urgency_level == 0


@pytest.mark.asyncio
async def test_set_duration_invalid():
    """Test setting invalid duration."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    with pytest.raises(ValueError, match="Duration must be a positive integer"):
        await service.set_duration(timer.id, 0)


@pytest.mark.asyncio
async def test_start_timer():
    """Test starting a timer."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    started = await service.start_timer(timer.id)
    assert started.status == TimerStatus.RUNNING


@pytest.mark.asyncio
async def test_start_timer_already_complete():
    """Test starting a completed timer."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    await repo.update(timer.id, elapsed_time=60, status=TimerStatus.COMPLETE)
    with pytest.raises(ValueError, match="already completed"):
        await service.start_timer(timer.id)


@pytest.mark.asyncio
async def test_stop_timer():
    """Test stopping a timer."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    stopped = await service.stop_timer(timer.id)
    assert stopped.status == TimerStatus.PAUSED


@pytest.mark.asyncio
async def test_reset_timer():
    """Test resetting a timer."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    await repo.update(timer.id, elapsed_time=30, status=TimerStatus.RUNNING)
    reset = await service.reset_timer(timer.id)
    assert reset.elapsed_time == 0
    assert reset.status == TimerStatus.IDLE
    assert reset.urgency_level == 0


@pytest.mark.asyncio
async def test_tick_timer():
    """Test incrementing timer by 1 second."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    await service.start_timer(timer.id)
    ticked = await service.tick_timer(timer.id)
    assert ticked.elapsed_time == 1
    assert ticked.status == TimerStatus.RUNNING


@pytest.mark.asyncio
async def test_tick_timer_reaches_duration():
    """Test timer completion on tick."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    await repo.update(timer.id, elapsed_time=59, status=TimerStatus.RUNNING)
    ticked = await service.tick_timer(timer.id)
    assert ticked.elapsed_time == 60
    assert ticked.status == TimerStatus.COMPLETE


@pytest.mark.asyncio
async def test_tick_timer_not_running():
    """Test ticking a paused timer does nothing."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(60)
    await repo.update(timer.id, elapsed_time=30, status=TimerStatus.PAUSED)
    ticked = await service.tick_timer(timer.id)
    assert ticked.elapsed_time == 30
    assert ticked.status == TimerStatus.PAUSED


@pytest.mark.asyncio
async def test_urgency_level_computation():
    """Test urgency level computation based on elapsed time."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(100)

    assert service._compute_urgency_level(0, 100) == 0
    assert service._compute_urgency_level(30, 100) == 0
    assert service._compute_urgency_level(33, 100) == 1
    assert service._compute_urgency_level(66, 100) == 2
    assert service._compute_urgency_level(90, 100) == 3
    assert service._compute_urgency_level(100, 100) == 3


@pytest.mark.asyncio
async def test_urgency_level_updates_on_tick():
    """Test urgency level updates during tick."""
    repo = MockTimerRepo()
    service = TimerService(repo)
    timer = await service.create_timer(100)
    await service.start_timer(timer.id)

    for _ in range(33):
        await service.tick_timer(timer.id)
    timer = await service.get_timer(timer.id)
    assert timer.urgency_level == 1

    for _ in range(33):
        await service.tick_timer(timer.id)
    timer = await service.get_timer(timer.id)
    assert timer.urgency_level == 2

    for _ in range(24):
        await service.tick_timer(timer.id)
    timer = await service.get_timer(timer.id)
    assert timer.urgency_level == 3
