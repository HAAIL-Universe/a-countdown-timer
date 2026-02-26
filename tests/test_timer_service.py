import pytest
from unittest.mock import AsyncMock
from uuid import UUID, uuid4
from datetime import datetime

from app.services.timer_service import TimerService
from app.models.timer import Timer, TimerStatus


@pytest.fixture
def mock_repo() -> AsyncMock:
    """Mock repository with async methods."""
    return AsyncMock()


@pytest.fixture
def service(mock_repo: AsyncMock) -> TimerService:
    """TimerService instance with mocked repo."""
    return TimerService(repo=mock_repo)


class TestComputeUrgency:
    """Tests for compute_urgency business logic."""

    def test_compute_urgency_levels(self, service: TimerService) -> None:
        """Urgency: 0–33%=0, 33–66%=1, 66–90%=2, 90%+=3."""
        duration = 100

        assert service.compute_urgency(0, duration) == 0
        assert service.compute_urgency(33, duration) == 0
        assert service.compute_urgency(34, duration) == 1
        assert service.compute_urgency(66, duration) == 1
        assert service.compute_urgency(67, duration) == 2
        assert service.compute_urgency(90, duration) == 2
        assert service.compute_urgency(91, duration) == 3
        assert service.compute_urgency(100, duration) == 3

    def test_compute_urgency_zero_duration(self, service: TimerService) -> None:
        """Zero duration returns urgency 0."""
        assert service.compute_urgency(0, 0) == 0
        assert service.compute_urgency(10, 0) == 0

    def test_compute_urgency_edge_boundaries(self, service: TimerService) -> None:
        """Test exact boundary transitions."""
        duration = 100
        assert service.compute_urgency(32, duration) == 0
        assert service.compute_urgency(33, duration) == 0
        assert service.compute_urgency(65, duration) == 1
        assert service.compute_urgency(66, duration) == 1
        assert service.compute_urgency(89, duration) == 2
        assert service.compute_urgency(90, duration) == 2


class TestCreateTimer:
    """Tests for timer creation."""

    @pytest.mark.asyncio
    async def test_create_timer_sets_idle_status(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """TimerService.create_timer calls repo.create and returns idle Timer."""
        duration = 60
        timer_id = uuid4()
        now = datetime.now()
        expected_timer = Timer(
            id=timer_id,
            duration=duration,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.create.return_value = expected_timer

        result = await service.create_timer(duration)

        mock_repo.create.assert_called_once_with(duration)
        assert result.status == TimerStatus.idle
        assert result.elapsed_time == 0
        assert result.id == timer_id


class TestStartTimer:
    """Tests for starting a timer."""

    @pytest.mark.asyncio
    async def test_start_timer_sets_running_status(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """Starting a timer sets status to running and computes urgency."""
        timer_id = uuid4()
        now = datetime.now()
        existing_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=10,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        updated_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=10,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = existing_timer
        mock_repo.update.return_value = updated_timer

        result = await service.start_timer(timer_id)

        mock_repo.get_by_id.assert_called_once_with(timer_id)
        assert result.status == TimerStatus.running
        mock_repo.update.assert_called_once_with(timer_id, 10, TimerStatus.running, 0)

    @pytest.mark.asyncio
    async def test_start_timer_not_found(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """Starting non-existent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.start_timer(timer_id)

        assert result is None


class TestStopTimer:
    """Tests for pausing a timer."""

    @pytest.mark.asyncio
    async def test_stop_timer_sets_paused_status(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """Stopping a timer sets status to paused."""
        timer_id = uuid4()
        now = datetime.now()
        existing_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=25,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        paused_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=25,
            status=TimerStatus.paused,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = existing_timer
        mock_repo.update.return_value = paused_timer

        result = await service.stop_timer(timer_id)

        mock_repo.get_by_id.assert_called_once_with(timer_id)
        assert result.status == TimerStatus.paused
        mock_repo.update.assert_called_once_with(timer_id, 25, TimerStatus.paused, 0)

    @pytest.mark.asyncio
    async def test_stop_timer_not_found(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """Stopping non-existent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.stop_timer(timer_id)

        assert result is None


class TestResetTimer:
    """Tests for resetting a timer."""

    @pytest.mark.asyncio
    async def test_reset_timer_clears_elapsed_time(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """Resetting a timer sets elapsed_time to 0 and status to idle."""
        timer_id = uuid4()
        now = datetime.now()
        existing_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=50,
            status=TimerStatus.paused,
            urgency_level=1,
            created_at=now,
            updated_at=now,
        )
        reset_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = existing_timer
        mock_repo.update.return_value = reset_timer

        result = await service.reset_timer(timer_id)

        mock_repo.get_by_id.assert_called_once_with(timer_id)
        assert result.elapsed_time == 0
        assert result.status == TimerStatus.idle
        mock_repo.update.assert_called_once_with(timer_id, 0, TimerStatus.idle, 0)

    @pytest.mark.asyncio
    async def test_reset_timer_not_found(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """Resetting non-existent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.reset_timer(timer_id)

        assert result is None


class TestTickTimer:
    """Tests for timer tick (increment elapsed time)."""

    @pytest.mark.asyncio
    async def test_tick_timer_increments_elapsed_time(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """Ticking a timer increments elapsed_time by 1."""
        timer_id = uuid4()
        now = datetime.now()
        existing_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=10,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        ticked_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=11,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = existing_timer
        mock_repo.update.return_value = ticked_timer

        result = await service.tick_timer(timer_id)

        assert result.elapsed_time == 11
        mock_repo.update.assert_called_once_with(timer_id, 11, TimerStatus.running, 0)

    @pytest.mark.asyncio
    async def test_tick_timer_completes_when_elapsed_equals_duration(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """Ticking a timer at duration boundary marks it complete."""
        timer_id = uuid4()
        now = datetime.now()
        existing_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=99,
            status=TimerStatus.running,
            urgency_level=3,
            created_at=now,
            updated_at=now,
        )
        completed_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=100,
            status=TimerStatus.complete,
            urgency_level=3,
            created_at=now,
            updated_at=now,
        )
        mock_repo.get_by_id.return_value = existing_timer
        mock_repo.update.return_value = completed_timer

        result = await service.tick_timer(timer_id)

        assert result.status == TimerStatus.complete
        assert result.elapsed_time == 100
        mock_repo.update.assert_called_once_with(timer_id, 100, TimerStatus.complete, 3)

    @pytest.mark.asyncio
    async def test_tick_timer_not_found(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """Ticking non-existent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.tick_timer(timer_id)

        assert result is None


class TestListTimers:
    """Tests for listing all timers."""

    @pytest.mark.asyncio
    async def test_list_timers_returns_all(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """list_timers calls repo and returns list."""
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
        assert result == timers
        mock_repo.list_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_timers_empty(self, service: TimerService, mock_repo: AsyncMock) -> None:
        """list_timers returns empty list when no timers exist."""
        mock_repo.list_all.return_value = []

        result = await service.list_timers()

        assert result == []
