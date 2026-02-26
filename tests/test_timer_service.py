import pytest
from uuid import UUID, uuid4
from datetime import datetime
from unittest.mock import AsyncMock

from app.services.timer_service import TimerService
from app.models.timer import Timer, TimerStatus
from app.repos.timer_repo import TimerRepo


@pytest.fixture
def mock_repo() -> AsyncMock:
    """Mock repository with async methods."""
    return AsyncMock(spec=TimerRepo)


@pytest.fixture
def service(mock_repo: AsyncMock) -> TimerService:
    """TimerService instance with mocked repo."""
    return TimerService(repo=mock_repo)


@pytest.fixture
def sample_timer() -> Timer:
    """Sample timer for testing."""
    timer_id = uuid4()
    return Timer(
        id=timer_id,
        duration=100,
        elapsed_time=0,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


class TestComputeUrgency:
    """Test urgency level computation logic."""

    def test_compute_urgency_levels(self, service: TimerService):
        """Urgency: 0 (0–33%), 1 (33–66%), 2 (66–90%), 3 (90%+)."""
        # 0% elapsed
        assert service.compute_urgency(0, 100) == 0
        # 30% elapsed (< 33%)
        assert service.compute_urgency(30, 100) == 0
        # 33% elapsed (boundary)
        assert service.compute_urgency(33, 100) == 1
        # 50% elapsed (33–66%)
        assert service.compute_urgency(50, 100) == 1
        # 66% elapsed (boundary)
        assert service.compute_urgency(66, 100) == 2
        # 80% elapsed (66–90%)
        assert service.compute_urgency(80, 100) == 2
        # 90% elapsed (boundary)
        assert service.compute_urgency(90, 100) == 3
        # 95% elapsed (90%+)
        assert service.compute_urgency(95, 100) == 3
        # 100% elapsed
        assert service.compute_urgency(100, 100) == 3

    def test_compute_urgency_zero_duration(self, service: TimerService):
        """When duration is 0, urgency is 0."""
        assert service.compute_urgency(0, 0) == 0
        assert service.compute_urgency(100, 0) == 0


class TestCreateTimer:
    """Test timer creation."""

    @pytest.mark.asyncio
    async def test_create_timer_sets_idle_status(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ):
        """TimerRepo.create inserts a row with status=idle and elapsed_time=0."""
        # Setup mock to return a timer with idle status
        idle_timer = Timer(
            id=uuid4(),
            duration=100,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.create.return_value = idle_timer

        # Call service
        result = await service.create_timer(duration=100)

        # Verify
        assert result is not None
        assert result.status == TimerStatus.idle
        assert result.elapsed_time == 0
        assert result.duration == 100
        assert isinstance(result.id, UUID)
        mock_repo.create.assert_called_once_with(100)


class TestStartTimer:
    """Test timer start transitions."""

    @pytest.mark.asyncio
    async def test_start_timer_sets_running_status(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ):
        """TimerService.start_timer transitions timer to running status."""
        # Setup mock: get_by_id returns idle timer, update returns running timer
        idle_timer = Timer(
            id=sample_timer.id,
            duration=100,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        running_timer = Timer(
            id=sample_timer.id,
            duration=100,
            elapsed_time=0,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=idle_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = idle_timer
        mock_repo.update.return_value = running_timer

        # Call service
        result = await service.start_timer(sample_timer.id)

        # Verify
        assert result is not None
        assert result.status == TimerStatus.running
        mock_repo.get_by_id.assert_called_once_with(sample_timer.id)
        mock_repo.update.assert_called_once_with(
            sample_timer.id,
            elapsed_time=0,
            status=TimerStatus.running,
            urgency_level=0,
        )

    @pytest.mark.asyncio
    async def test_start_timer_returns_none_if_timer_not_found(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """TimerService.start_timer returns None if timer does not exist."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.start_timer(timer_id)

        assert result is None
        mock_repo.get_by_id.assert_called_once_with(timer_id)
        mock_repo.update.assert_not_called()


class TestStopTimer:
    """Test timer pause transitions."""

    @pytest.mark.asyncio
    async def test_stop_timer_sets_paused_status(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ):
        """TimerService.stop_timer transitions timer to paused status."""
        # Setup mock
        running_timer = Timer(
            id=sample_timer.id,
            duration=100,
            elapsed_time=50,
            status=TimerStatus.running,
            urgency_level=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        paused_timer = Timer(
            id=sample_timer.id,
            duration=100,
            elapsed_time=50,
            status=TimerStatus.paused,
            urgency_level=1,
            created_at=running_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = running_timer
        mock_repo.update.return_value = paused_timer

        # Call service
        result = await service.stop_timer(sample_timer.id)

        # Verify
        assert result is not None
        assert result.status == TimerStatus.paused
        assert result.elapsed_time == 50
        mock_repo.get_by_id.assert_called_once_with(sample_timer.id)
        mock_repo.update.assert_called_once_with(
            sample_timer.id,
            elapsed_time=50,
            status=TimerStatus.paused,
            urgency_level=1,
        )

    @pytest.mark.asyncio
    async def test_stop_timer_returns_none_if_timer_not_found(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """TimerService.stop_timer returns None if timer does not exist."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.stop_timer(timer_id)

        assert result is None
        mock_repo.get_by_id.assert_called_once_with(timer_id)
        mock_repo.update.assert_not_called()


class TestResetTimer:
    """Test timer reset."""

    @pytest.mark.asyncio
    async def test_reset_timer_clears_elapsed_time(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ):
        """TimerService.reset_timer clears elapsed time and sets idle status."""
        # Setup mock
        running_timer = Timer(
            id=sample_timer.id,
            duration=100,
            elapsed_time=75,
            status=TimerStatus.running,
            urgency_level=2,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        reset_timer = Timer(
            id=sample_timer.id,
            duration=100,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=running_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = running_timer
        mock_repo.update.return_value = reset_timer

        # Call service
        result = await service.reset_timer(sample_timer.id)

        # Verify
        assert result is not None
        assert result.elapsed_time == 0
        assert result.status == TimerStatus.idle
        assert result.urgency_level == 0
        mock_repo.get_by_id.assert_called_once_with(sample_timer.id)
        mock_repo.update.assert_called_once_with(
            sample_timer.id,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
        )

    @pytest.mark.asyncio
    async def test_reset_timer_returns_none_if_timer_not_found(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """TimerService.reset_timer returns None if timer does not exist."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await service.reset_timer(timer_id)

        assert result is None
        mock_repo.get_by_id.assert_called_once_with(timer_id)
        mock_repo.update.assert_not_called()


class TestTickTimer:
    """Test timer tick (increment elapsed time)."""

    @pytest.mark.asyncio
    async def test_tick_timer_increments_elapsed_time(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ):
        """TimerService.tick_timer increments elapsed_time by 1 second."""
        # Setup mock
        running_timer = Timer(
            id=sample_timer.id,
            duration=100,
            elapsed_time=49,
            status=TimerStatus.running,
            urgency_level=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        ticked_timer = Timer(
            id=sample_timer.id,
            duration=100,
            elapsed_time=50,
            status=TimerStatus.running,
            urgency_level=1,
            created_at=running_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = running_timer
        mock_repo.update.return_value = ticked_timer

        # Call service
        result = await service.tick_timer(sample_timer.id)

        # Verify
        assert result is not None
        assert result.elapsed_time == 50
        assert result.status == TimerStatus.running
        mock_repo.update.assert_called_once_with(
            sample_timer.id,
            elapsed_time=50,
            status=TimerStatus.running,
            urgency_level=1,
        )

    @pytest.mark.asyncio
    async def test_tick_timer_marks_complete_when_elapsed_exceeds_duration(
        self, service: TimerService, mock_repo: AsyncMock, sample_timer: Timer
    ):
        """TimerService.tick_timer marks timer complete when elapsed >= duration."""
        # Setup mock
        almost_done_timer = Timer(
            id=sample_timer.id,
            duration=100,
            elapsed_time=99,
            status=TimerStatus.running,
            urgency_level=3,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        complete_timer = Timer(
            id=sample_timer.id,
            duration=100,
            elapsed_time=100,
            status=TimerStatus.complete,
            urgency_level=3,
            created_at=almost_done_timer.created_at,
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = almost_done_timer
        mock_repo.update.return_value = complete_timer

        # Call service
        result = await service.tick_timer(sample_timer.id)

        # Verify
        assert result is not None
        assert result.elapsed_time == 100
        assert result.status == TimerStatus.complete
        mock_repo.update.assert_called_once_with(
            sample_timer.id,
            elapsed_time=100,
            status=TimerStatus.complete,
            urgency_level=3,
        )


class TestListTimers:
    """Test listing all timers."""

    @pytest.mark.asyncio
    async def test_list_timers_returns_all_timers(
        self, service: TimerService, mock_repo: AsyncMock
    ):
        """TimerService.list_timers returns all timers from repo."""
        # Setup mock
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

        # Call service
        result = await service.list_timers()

        # Verify
        assert result is not None
        assert len(result) == 2
        assert result[0].status == TimerStatus.idle
        assert result[1].status == TimerStatus.running
        mock_repo.list_all.assert_called_once()
