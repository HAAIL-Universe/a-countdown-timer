import pytest
from uuid import UUID, uuid4
from unittest.mock import AsyncMock
from datetime import datetime

from app.services.timer_service import TimerService
from app.models.timer import Timer, TimerStatus


@pytest.fixture
def mock_repo() -> AsyncMock:
    """Mock repository with async methods."""
    repo = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repo: AsyncMock) -> TimerService:
    """TimerService instance with mocked repo."""
    return TimerService(repo=mock_repo)


@pytest.fixture
def sample_timer() -> Timer:
    """Sample timer instance for testing."""
    return Timer(
        id=uuid4(),
        duration=100,
        elapsed_time=0,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


class TestComputeUrgency:
    """Test urgency level computation logic."""

    def test_compute_urgency_0_percent_elapsed(self, service: TimerService):
        """Urgency 0 for 0% elapsed (< 33%)."""
        urgency = service.compute_urgency(0, 100)
        assert urgency == 0

    def test_compute_urgency_32_percent_elapsed(self, service: TimerService):
        """Urgency 0 for 32% elapsed (< 33%)."""
        urgency = service.compute_urgency(32, 100)
        assert urgency == 0

    def test_compute_urgency_33_percent_elapsed(self, service: TimerService):
        """Urgency 1 for 33% elapsed (>= 33% and < 66%)."""
        urgency = service.compute_urgency(33, 100)
        assert urgency == 1

    def test_compute_urgency_50_percent_elapsed(self, service: TimerService):
        """Urgency 1 for 50% elapsed (>= 33% and < 66%)."""
        urgency = service.compute_urgency(50, 100)
        assert urgency == 1

    def test_compute_urgency_65_percent_elapsed(self, service: TimerService):
        """Urgency 1 for 65% elapsed (>= 33% and < 66%)."""
        urgency = service.compute_urgency(65, 100)
        assert urgency == 1

    def test_compute_urgency_66_percent_elapsed(self, service: TimerService):
        """Urgency 2 for 66% elapsed (>= 66% and < 90%)."""
        urgency = service.compute_urgency(66, 100)
        assert urgency == 2

    def test_compute_urgency_89_percent_elapsed(self, service: TimerService):
        """Urgency 2 for 89% elapsed (>= 66% and < 90%)."""
        urgency = service.compute_urgency(89, 100)
        assert urgency == 2

    def test_compute_urgency_90_percent_elapsed(self, service: TimerService):
        """Urgency 3 for 90% elapsed (>= 90%)."""
        urgency = service.compute_urgency(90, 100)
        assert urgency == 3

    def test_compute_urgency_100_percent_elapsed(self, service: TimerService):
        """Urgency 3 for 100% elapsed."""
        urgency = service.compute_urgency(100, 100)
        assert urgency == 3

    def test_compute_urgency_zero_duration(self, service: TimerService):
        """Urgency 0 for zero or negative duration."""
        assert service.compute_urgency(10, 0) == 0
        assert service.compute_urgency(10, -1) == 0


class TestCreateTimer:
    """Test timer creation."""

    @pytest.mark.asyncio
    async def test_create_timer_sets_idle_status(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ):
        """TimerService.create_timer calls repo.create and returns Timer."""
        expected_timer = Timer(
            id=uuid4(),
            duration=60,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.create.return_value = expected_timer

        result = await service.create_timer(duration=60)

        assert result.duration == 60
        assert result.status == TimerStatus.idle
        assert result.elapsed_time == 0
        assert result.urgency_level == 0
        mock_repo.create.assert_called_once_with(60)


class TestStartTimer:
    """Test timer start transitions."""

    @pytest.mark.asyncio
    async def test_start_timer_sets_running_status(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """Starting an idle timer transitions to running status."""
        idle_timer = Timer(
            id=uuid4(),
            duration=100,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        running_timer = Timer(
            id=idle_timer.id,
            duration=100,
            elapsed_time=0,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=idle_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = idle_timer
        mock_repo.update.return_value = running_timer

        result = await service.start_timer(idle_timer.id)

        assert result.status == TimerStatus.running
        mock_repo.get_by_id.assert_called_once_with(idle_timer.id)
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_timer_returns_none_for_nonexistent(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """Starting a nonexistent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.start_timer(timer_id)

        assert result is None

    @pytest.mark.asyncio
    async def test_start_timer_from_paused_status(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """Starting a paused timer transitions to running."""
        paused_timer = Timer(
            id=uuid4(),
            duration=100,
            elapsed_time=50,
            status=TimerStatus.paused,
            urgency_level=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        running_timer = Timer(
            id=paused_timer.id,
            duration=100,
            elapsed_time=50,
            status=TimerStatus.running,
            urgency_level=1,
            created_at=paused_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = paused_timer
        mock_repo.update.return_value = running_timer

        result = await service.start_timer(paused_timer.id)

        assert result.status == TimerStatus.running


class TestStopTimer:
    """Test timer stop (pause) transitions."""

    @pytest.mark.asyncio
    async def test_stop_timer_sets_paused_status(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """Stopping a running timer transitions to paused status."""
        running_timer = Timer(
            id=uuid4(),
            duration=100,
            elapsed_time=50,
            status=TimerStatus.running,
            urgency_level=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        paused_timer = Timer(
            id=running_timer.id,
            duration=100,
            elapsed_time=50,
            status=TimerStatus.paused,
            urgency_level=1,
            created_at=running_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = running_timer
        mock_repo.update.return_value = paused_timer

        result = await service.stop_timer(running_timer.id)

        assert result.status == TimerStatus.paused
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_timer_returns_none_for_nonexistent(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """Stopping a nonexistent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.stop_timer(timer_id)

        assert result is None


class TestResetTimer:
    """Test timer reset transitions."""

    @pytest.mark.asyncio
    async def test_reset_timer_clears_elapsed_time(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """Resetting a timer sets elapsed_time to 0 and status to idle."""
        active_timer = Timer(
            id=uuid4(),
            duration=100,
            elapsed_time=75,
            status=TimerStatus.running,
            urgency_level=2,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        reset_timer = Timer(
            id=active_timer.id,
            duration=100,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=active_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = active_timer
        mock_repo.update.return_value = reset_timer

        result = await service.reset_timer(active_timer.id)

        assert result.elapsed_time == 0
        assert result.status == TimerStatus.idle
        assert result.urgency_level == 0
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_reset_timer_returns_none_for_nonexistent(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """Resetting a nonexistent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.reset_timer(timer_id)

        assert result is None


class TestTickTimer:
    """Test timer tick (increment) logic."""

    @pytest.mark.asyncio
    async def test_tick_timer_increments_elapsed(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """Ticking a running timer increments elapsed_time by 1."""
        running_timer = Timer(
            id=uuid4(),
            duration=100,
            elapsed_time=49,
            status=TimerStatus.running,
            urgency_level=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        ticked_timer = Timer(
            id=running_timer.id,
            duration=100,
            elapsed_time=50,
            status=TimerStatus.running,
            urgency_level=1,
            created_at=running_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = running_timer
        mock_repo.update.return_value = ticked_timer

        result = await service.tick_timer(running_timer.id)

        assert result.elapsed_time == 50

    @pytest.mark.asyncio
    async def test_tick_timer_completes_when_elapsed_reaches_duration(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """Ticking to elapsed >= duration transitions to complete."""
        running_timer = Timer(
            id=uuid4(),
            duration=100,
            elapsed_time=99,
            status=TimerStatus.running,
            urgency_level=3,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        complete_timer = Timer(
            id=running_timer.id,
            duration=100,
            elapsed_time=100,
            status=TimerStatus.complete,
            urgency_level=3,
            created_at=running_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = running_timer
        mock_repo.update.return_value = complete_timer

        result = await service.tick_timer(running_timer.id)

        assert result.status == TimerStatus.complete
        assert result.elapsed_time == 100


class TestListTimers:
    """Test listing all timers."""

    @pytest.mark.asyncio
    async def test_list_timers_returns_all(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """Listing timers returns all timers from repo."""
        timers = [
            Timer(
                id=uuid4(),
                duration=100,
                elapsed_time=0,
                status=TimerStatus.idle,
                urgency_level=0,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Timer(
                id=uuid4(),
                duration=60,
                elapsed_time=30,
                status=TimerStatus.running,
                urgency_level=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]
        mock_repo.list_all.return_value = timers

        result = await service.list_timers()

        assert len(result) == 2
        assert result[0].status == TimerStatus.idle
        assert result[1].status == TimerStatus.running
        mock_repo.list_all.assert_called_once()
