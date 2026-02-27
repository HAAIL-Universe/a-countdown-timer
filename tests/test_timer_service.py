import pytest
from uuid import UUID, uuid4
from datetime import datetime
from unittest.mock import AsyncMock
from app.services.timer_service import TimerService
from app.models.timer import Timer, TimerStatus


@pytest.fixture
def mock_repo() -> AsyncMock:
    """Mock TimerRepo for testing TimerService."""
    return AsyncMock()


@pytest.fixture
def service(mock_repo: AsyncMock) -> TimerService:
    """TimerService instance with mocked repo."""
    return TimerService(repo=mock_repo)


@pytest.fixture
def sample_timer() -> Timer:
    """Sample Timer instance for testing."""
    now = datetime.now()
    return Timer(
        id=uuid4(),
        duration=100,
        elapsed_time=0,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=now,
        updated_at=now,
    )


@pytest.mark.asyncio
async def test_compute_urgency_levels(service: TimerService):
    """TimerService.compute_urgency returns correct levels based on elapsed_time/duration ratio."""
    # 0–33% elapsed → urgency 0
    assert service.compute_urgency(0, 100) == 0
    assert service.compute_urgency(32, 100) == 0
    assert service.compute_urgency(33, 100) == 0

    # 33–66% elapsed → urgency 1
    assert service.compute_urgency(34, 100) == 1
    assert service.compute_urgency(50, 100) == 1
    assert service.compute_urgency(65, 100) == 1

    # 66–90% elapsed → urgency 2
    assert service.compute_urgency(66, 100) == 2
    assert service.compute_urgency(75, 100) == 2
    assert service.compute_urgency(89, 100) == 2

    # 90%+ elapsed → urgency 3
    assert service.compute_urgency(90, 100) == 3
    assert service.compute_urgency(95, 100) == 3
    assert service.compute_urgency(100, 100) == 3

    # Edge case: duration <= 0 returns 0
    assert service.compute_urgency(10, 0) == 0
    assert service.compute_urgency(10, -1) == 0


@pytest.mark.asyncio
async def test_create_timer_sets_idle_status(
    service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
):
    """TimerRepo.create inserts a row with status=idle and elapsed_time=0."""
    created_timer = Timer(
        id=uuid4(),
        duration=60,
        elapsed_time=0,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_repo.create.return_value = created_timer

    result = await service.create_timer(60)

    assert result.status == TimerStatus.idle
    assert result.elapsed_time == 0
    assert isinstance(result.id, UUID)
    mock_repo.create.assert_called_once_with(60)


@pytest.mark.asyncio
async def test_start_timer_sets_running_status(
    service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
):
    """Starting a timer changes status to running and recomputes urgency."""
    timer_id = uuid4()
    mock_repo.get_by_id.return_value = sample_timer

    updated_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=0,
        status=TimerStatus.running,
        urgency_level=0,
        created_at=sample_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.update.return_value = updated_timer

    result = await service.start_timer(timer_id)

    assert result.status == TimerStatus.running
    mock_repo.get_by_id.assert_called_once_with(timer_id)
    mock_repo.update.assert_called_once_with(timer_id, 0, TimerStatus.running, 0)


@pytest.mark.asyncio
async def test_stop_timer_sets_paused_status(
    service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
):
    """Stopping a timer changes status to paused and recomputes urgency."""
    timer_id = uuid4()
    running_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=50,
        status=TimerStatus.running,
        urgency_level=1,
        created_at=sample_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.get_by_id.return_value = running_timer

    paused_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=50,
        status=TimerStatus.paused,
        urgency_level=1,
        created_at=running_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.update.return_value = paused_timer

    result = await service.stop_timer(timer_id)

    assert result.status == TimerStatus.paused
    assert result.elapsed_time == 50
    mock_repo.get_by_id.assert_called_once_with(timer_id)
    mock_repo.update.assert_called_once_with(timer_id, 50, TimerStatus.paused, 1)


@pytest.mark.asyncio
async def test_reset_timer_clears_elapsed_time(
    service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
):
    """Resetting a timer sets elapsed_time=0 and status=idle."""
    timer_id = uuid4()
    running_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=75,
        status=TimerStatus.running,
        urgency_level=2,
        created_at=sample_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.get_by_id.return_value = running_timer

    reset_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=0,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=running_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.update.return_value = reset_timer

    result = await service.reset_timer(timer_id)

    assert result.elapsed_time == 0
    assert result.status == TimerStatus.idle
    assert result.urgency_level == 0
    mock_repo.get_by_id.assert_called_once_with(timer_id)
    mock_repo.update.assert_called_once_with(timer_id, 0, TimerStatus.idle, 0)


@pytest.mark.asyncio
async def test_tick_timer_increments_elapsed_time(
    service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
):
    """Ticking a timer increments elapsed_time by 1 second."""
    timer_id = uuid4()
    ticking_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=10,
        status=TimerStatus.running,
        urgency_level=0,
        created_at=sample_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.get_by_id.return_value = ticking_timer

    ticked_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=11,
        status=TimerStatus.running,
        urgency_level=0,
        created_at=ticking_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.update.return_value = ticked_timer

    result = await service.tick_timer(timer_id)

    assert result.elapsed_time == 11
    mock_repo.update.assert_called_once_with(timer_id, 11, TimerStatus.running, 0)


@pytest.mark.asyncio
async def test_tick_timer_caps_at_duration(
    service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
):
    """Ticking a timer at duration marks it complete."""
    timer_id = uuid4()
    near_complete_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=99,
        status=TimerStatus.running,
        urgency_level=3,
        created_at=sample_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.get_by_id.return_value = near_complete_timer

    complete_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=100,
        status=TimerStatus.complete,
        urgency_level=3,
        created_at=near_complete_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.update.return_value = complete_timer

    result = await service.tick_timer(timer_id)

    assert result.elapsed_time == 100
    assert result.status == TimerStatus.complete
    mock_repo.update.assert_called_once_with(timer_id, 100, TimerStatus.complete, 3)


@pytest.mark.asyncio
async def test_list_timers_returns_all_timers(
    service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
):
    """Listing timers returns all timers from the repo."""
    now = datetime.now()
    timers = [
        Timer(
            id=uuid4(),
            duration=60,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        ),
        Timer(
            id=uuid4(),
            duration=120,
            elapsed_time=30,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        ),
    ]
    mock_repo.list_all.return_value = timers

    result = await service.list_timers()

    assert len(result) == 2
    assert result[0].duration == 60
    assert result[1].duration == 120
    mock_repo.list_all.assert_called_once()


@pytest.mark.asyncio
async def test_start_timer_returns_none_if_not_found(
    service: TimerService, mock_repo: AsyncMock
):
    """Starting a non-existent timer returns None."""
    timer_id = uuid4()
    mock_repo.get_by_id.return_value = None

    result = await service.start_timer(timer_id)

    assert result is None
    mock_repo.get_by_id.assert_called_once_with(timer_id)
    mock_repo.update.assert_not_called()


@pytest.mark.asyncio
async def test_stop_timer_returns_none_if_not_found(
    service: TimerService, mock_repo: AsyncMock
):
    """Stopping a non-existent timer returns None."""
    timer_id = uuid4()
    mock_repo.get_by_id.return_value = None

    result = await service.stop_timer(timer_id)

    assert result is None
    mock_repo.get_by_id.assert_called_once_with(timer_id)
    mock_repo.update.assert_not_called()


@pytest.mark.asyncio
async def test_reset_timer_returns_none_if_not_found(
    service: TimerService, mock_repo: AsyncMock
):
    """Resetting a non-existent timer returns None."""
    timer_id = uuid4()
    mock_repo.get_by_id.return_value = None

    result = await service.reset_timer(timer_id)

    assert result is None
    mock_repo.get_by_id.assert_called_once_with(timer_id)
    mock_repo.update.assert_not_called()


@pytest.mark.asyncio
async def test_tick_timer_returns_none_if_not_found(
    service: TimerService, mock_repo: AsyncMock
):
    """Ticking a non-existent timer returns None."""
    timer_id = uuid4()
    mock_repo.get_by_id.return_value = None

    result = await service.tick_timer(timer_id)

    assert result is None
    mock_repo.get_by_id.assert_called_once_with(timer_id)
    mock_repo.update.assert_not_called()


@pytest.mark.asyncio
async def test_urgency_computation_with_paused_timer(
    service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
):
    """Urgency is correctly recomputed when a paused timer is resumed."""
    timer_id = uuid4()
    paused_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=80,
        status=TimerStatus.paused,
        urgency_level=2,
        created_at=sample_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.get_by_id.return_value = paused_timer

    running_timer = Timer(
        id=timer_id,
        duration=100,
        elapsed_time=80,
        status=TimerStatus.running,
        urgency_level=3,
        created_at=paused_timer.created_at,
        updated_at=datetime.now(),
    )
    mock_repo.update.return_value = running_timer

    result = await service.start_timer(timer_id)

    assert result.urgency_level == 3
    assert result.status == TimerStatus.running
    mock_repo.update.assert_called_once_with(timer_id, 80, TimerStatus.running, 3)
