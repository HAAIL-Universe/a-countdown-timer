from datetime import datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepo
from app.services.timer_service import TimerService


@pytest.fixture
def mock_repo() -> AsyncMock:
    """Mock TimerRepo for isolation."""
    return AsyncMock(spec=TimerRepo)


@pytest.fixture
def service(mock_repo: AsyncMock) -> TimerService:
    """TimerService with mocked repo."""
    return TimerService(mock_repo)


@pytest.fixture
def sample_timer() -> Timer:
    """Sample Timer instance for testing."""
    now = datetime.utcnow()
    return Timer(
        id=uuid4(),
        duration=100,
        elapsed_time=0,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=now,
        updated_at=now,
    )


class TestComputeUrgency:
    """Test urgency computation logic."""

    def test_compute_urgency_levels(self, service: TimerService) -> None:
        """Urgency: 0 for 0–33%, 1 for 33–66%, 2 for 66–90%, 3 for 90%+."""
        assert service.compute_urgency(0, 100) == 0
        assert service.compute_urgency(32, 100) == 0
        assert service.compute_urgency(33, 100) == 1
        assert service.compute_urgency(50, 100) == 1
        assert service.compute_urgency(65, 100) == 1
        assert service.compute_urgency(66, 100) == 2
        assert service.compute_urgency(80, 100) == 2
        assert service.compute_urgency(89, 100) == 2
        assert service.compute_urgency(90, 100) == 3
        assert service.compute_urgency(100, 100) == 3

    def test_compute_urgency_zero_duration(self, service: TimerService) -> None:
        """Zero duration returns urgency 0."""
        assert service.compute_urgency(0, 0) == 0
        assert service.compute_urgency(10, 0) == 0

    def test_compute_urgency_negative_duration(self, service: TimerService) -> None:
        """Negative duration returns urgency 0."""
        assert service.compute_urgency(50, -100) == 0


class TestCreateTimer:
    """Test timer creation."""

    @pytest.mark.asyncio
    async def test_create_timer_sets_idle_status(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ) -> None:
        """Create returns Timer with idle status and elapsed_time=0."""
        expected = Timer(
            id=uuid4(),
            duration=60,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        mock_repo.create.return_value = expected

        result = await service.create_timer(60)

        assert result.status == TimerStatus.idle
        assert result.elapsed_time == 0
        assert result.duration == 60
        mock_repo.create.assert_called_once_with(60)

    @pytest.mark.asyncio
    async def test_create_timer_calls_repo(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ) -> None:
        """Create delegates to repo.create."""
        mock_repo.create.return_value = sample_timer

        await service.create_timer(100)

        mock_repo.create.assert_called_once_with(100)


class TestStartTimer:
    """Test timer start."""

    @pytest.mark.asyncio
    async def test_start_timer_sets_running_status(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ) -> None:
        """Start transitions timer to running status."""
        timer_id = sample_timer.id
        running_timer = Timer(
            id=timer_id,
            duration=sample_timer.duration,
            elapsed_time=0,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_by_id.return_value = sample_timer
        mock_repo.update.return_value = running_timer

        result = await service.start_timer(timer_id)

        assert result.status == TimerStatus.running
        mock_repo.get_by_id.assert_called_once_with(timer_id)
        mock_repo.update.assert_called_once_with(timer_id, 0, TimerStatus.running, 0)

    @pytest.mark.asyncio
    async def test_start_timer_nonexistent(
        self, service: TimerService, mock_repo: AsyncMock
    ) -> None:
        """Start nonexistent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.start_timer(timer_id)

        assert result is None

    @pytest.mark.asyncio
    async def test_start_timer_computes_urgency(
        self, service: TimerService, mock_repo: AsyncMock
    ) -> None:
        """Start computes urgency based on elapsed time."""
        timer_id = uuid4()
        now = datetime.utcnow()
        in_progress = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=50,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        started = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=50,
            status=TimerStatus.running,
            urgency_level=1,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = in_progress
        mock_repo.update.return_value = started

        result = await service.start_timer(timer_id)

        assert result.urgency_level == 1
        mock_repo.update.assert_called_once_with(timer_id, 50, TimerStatus.running, 1)


class TestStopTimer:
    """Test timer stop/pause."""

    @pytest.mark.asyncio
    async def test_stop_timer_sets_paused_status(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ) -> None:
        """Stop transitions timer to paused status."""
        timer_id = sample_timer.id
        paused_timer = Timer(
            id=timer_id,
            duration=sample_timer.duration,
            elapsed_time=0,
            status=TimerStatus.paused,
            urgency_level=0,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_by_id.return_value = sample_timer
        mock_repo.update.return_value = paused_timer

        result = await service.stop_timer(timer_id)

        assert result.status == TimerStatus.paused
        mock_repo.get_by_id.assert_called_once_with(timer_id)
        mock_repo.update.assert_called_once_with(timer_id, 0, TimerStatus.paused, 0)

    @pytest.mark.asyncio
    async def test_stop_timer_nonexistent(
        self, service: TimerService, mock_repo: AsyncMock
    ) -> None:
        """Stop nonexistent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.stop_timer(timer_id)

        assert result is None


class TestResetTimer:
    """Test timer reset."""

    @pytest.mark.asyncio
    async def test_reset_timer_clears_elapsed_time(
        self, service: TimerService, mock_repo: AsyncMock
    ) -> None:
        """Reset clears elapsed_time to 0 and sets status to idle."""
        timer_id = uuid4()
        now = datetime.utcnow()
        running = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=75,
            status=TimerStatus.running,
            urgency_level=2,
            created_at=now,
            updated_at=now,
        )
        idle_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = running
        mock_repo.update.return_value = idle_timer

        result = await service.reset_timer(timer_id)

        assert result.elapsed_time == 0
        assert result.status == TimerStatus.idle
        mock_repo.update.assert_called_once_with(timer_id, 0, TimerStatus.idle, 0)

    @pytest.mark.asyncio
    async def test_reset_timer_nonexistent(
        self, service: TimerService, mock_repo: AsyncMock
    ) -> None:
        """Reset nonexistent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.reset_timer(timer_id)

        assert result is None


class TestTickTimer:
    """Test timer increment."""

    @pytest.mark.asyncio
    async def test_tick_timer_increments_elapsed(
        self, service: TimerService, mock_repo: AsyncMock
    ) -> None:
        """Tick increments elapsed_time by 1."""
        timer_id = uuid4()
        now = datetime.utcnow()
        before = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=10,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        after = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=11,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = before
        mock_repo.update.return_value = after

        result = await service.tick_timer(timer_id)

        assert result.elapsed_time == 11
        mock_repo.update.assert_called_once_with(timer_id, 11, TimerStatus.running, 0)

    @pytest.mark.asyncio
    async def test_tick_timer_marks_complete_at_duration(
        self, service: TimerService, mock_repo: AsyncMock
    ) -> None:
        """Tick marks complete when elapsed_time >= duration."""
        timer_id = uuid4()
        now = datetime.utcnow()
        before = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=99,
            status=TimerStatus.running,
            urgency_level=3,
            created_at=now,
            updated_at=now,
        )
        completed = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=100,
            status=TimerStatus.complete,
            urgency_level=3,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = before
        mock_repo.update.return_value = completed

        result = await service.tick_timer(timer_id)

        assert result.status == TimerStatus.complete
        mock_repo.update.assert_called_once_with(timer_id, 100, TimerStatus.complete, 3)

    @pytest.mark.asyncio
    async def test_tick_timer_nonexistent(
        self, service: TimerService, mock_repo: AsyncMock
    ) -> None:
        """Tick nonexistent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.tick_timer(timer_id)

        assert result is None


class TestListTimers:
    """Test list operation."""

    @pytest.mark.asyncio
    async def test_list_timers(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ) -> None:
        """List returns all timers from repo."""
        mock_repo.list_all.return_value = [sample_timer]

        result = await service.list_timers()

        assert len(result) == 1
        assert result[0] == sample_timer
        mock_repo.list_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_timers_empty(
        self, service: TimerService, mock_repo: AsyncMock
    ) -> None:
        """List empty returns empty list."""
        mock_repo.list_all.return_value = []

        result = await service.list_timers()

        assert result == []
