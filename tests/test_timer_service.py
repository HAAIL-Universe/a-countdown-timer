import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from app.services.timer_service import TimerService
from app.models.timer import Timer, TimerStatus


@pytest.fixture
def mock_repo():
    """Create a mock TimerRepo for testing."""
    return AsyncMock()


@pytest.fixture
def timer_service(mock_repo):
    """Create a TimerService with mock repo."""
    return TimerService(mock_repo)


@pytest.fixture
def sample_timer():
    """Create a sample Timer instance for testing."""
    return Timer(
        id=uuid4(),
        duration=60,
        elapsed_time=0,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


class TestComputeUrgency:
    """Test urgency level computation."""

    def test_compute_urgency_level_0_at_0_percent(self, timer_service):
        """Urgency is 0 when elapsed time is 0% of duration."""
        assert timer_service.compute_urgency(0, 100) == 0

    def test_compute_urgency_level_0_at_33_percent(self, timer_service):
        """Urgency is 0 when elapsed time is 0–33% of duration."""
        assert timer_service.compute_urgency(33, 100) == 0
        assert timer_service.compute_urgency(32, 100) == 0

    def test_compute_urgency_level_1_at_50_percent(self, timer_service):
        """Urgency is 1 when elapsed time is 33–66% of duration."""
        assert timer_service.compute_urgency(50, 100) == 1
        assert timer_service.compute_urgency(33, 100) == 1
        assert timer_service.compute_urgency(65, 100) == 1

    def test_compute_urgency_level_2_at_75_percent(self, timer_service):
        """Urgency is 2 when elapsed time is 66–90% of duration."""
        assert timer_service.compute_urgency(75, 100) == 2
        assert timer_service.compute_urgency(66, 100) == 2
        assert timer_service.compute_urgency(89, 100) == 2

    def test_compute_urgency_level_3_at_90_percent(self, timer_service):
        """Urgency is 3 when elapsed time is 90%+ of duration."""
        assert timer_service.compute_urgency(90, 100) == 3
        assert timer_service.compute_urgency(95, 100) == 3
        assert timer_service.compute_urgency(100, 100) == 3

    def test_compute_urgency_with_zero_duration(self, timer_service):
        """Urgency is 0 when duration is zero or negative."""
        assert timer_service.compute_urgency(10, 0) == 0
        assert timer_service.compute_urgency(10, -1) == 0

    def test_compute_urgency_boundary_33_percent(self, timer_service):
        """Urgency transitions from 0 to 1 at 33% boundary."""
        assert timer_service.compute_urgency(32, 100) == 0
        assert timer_service.compute_urgency(33, 100) == 1

    def test_compute_urgency_boundary_66_percent(self, timer_service):
        """Urgency transitions from 1 to 2 at 66% boundary."""
        assert timer_service.compute_urgency(65, 100) == 1
        assert timer_service.compute_urgency(66, 100) == 2

    def test_compute_urgency_boundary_90_percent(self, timer_service):
        """Urgency transitions from 2 to 3 at 90% boundary."""
        assert timer_service.compute_urgency(89, 100) == 2
        assert timer_service.compute_urgency(90, 100) == 3


class TestCreateTimer:
    """Test timer creation."""

    @pytest.mark.asyncio
    async def test_create_timer_sets_idle_status(self, timer_service, mock_repo, sample_timer):
        """Create timer sets status to idle and elapsed_time to 0."""
        mock_repo.create.return_value = sample_timer
        result = await timer_service.create_timer(60)
        mock_repo.create.assert_called_once_with(60)
        assert result.status == TimerStatus.idle
        assert result.elapsed_time == 0
        assert result.urgency_level == 0


class TestStartTimer:
    """Test starting a timer."""

    @pytest.mark.asyncio
    async def test_start_timer_changes_status_to_running(self, timer_service, mock_repo, sample_timer):
        """Starting a timer changes status to running."""
        running_timer = sample_timer.model_copy(update={"status": TimerStatus.running})
        mock_repo.get_by_id.return_value = sample_timer
        mock_repo.update.return_value = running_timer
        result = await timer_service.start_timer(sample_timer.id)
        assert result.status == TimerStatus.running
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_timer_returns_none_if_not_found(self, timer_service, mock_repo):
        """Starting a non-existent timer returns None."""
        mock_repo.get_by_id.return_value = None
        result = await timer_service.start_timer(uuid4())
        assert result is None

    @pytest.mark.asyncio
    async def test_start_timer_updates_urgency(self, timer_service, mock_repo):
        """Starting a timer with elapsed time updates urgency level."""
        timer = Timer(
            id=uuid4(),
            duration=100,
            elapsed_time=50,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        running_timer = timer.model_copy(update={"status": TimerStatus.running, "urgency_level": 1})
        mock_repo.get_by_id.return_value = timer
        mock_repo.update.return_value = running_timer
        result = await timer_service.start_timer(timer.id)
        assert result.urgency_level == 1


class TestStopTimer:
    """Test stopping/pausing a timer."""

    @pytest.mark.asyncio
    async def test_stop_timer_changes_status_to_paused(self, timer_service, mock_repo, sample_timer):
        """Stopping a timer changes status to paused."""
        paused_timer = sample_timer.model_copy(update={"status": TimerStatus.paused})
        mock_repo.get_by_id.return_value = sample_timer
        mock_repo.update.return_value = paused_timer
        result = await timer_service.stop_timer(sample_timer.id)
        assert result.status == TimerStatus.paused
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_timer_returns_none_if_not_found(self, timer_service, mock_repo):
        """Stopping a non-existent timer returns None."""
        mock_repo.get_by_id.return_value = None
        result = await timer_service.stop_timer(uuid4())
        assert result is None

    @pytest.mark.asyncio
    async def test_stop_timer_preserves_elapsed_time(self, timer_service, mock_repo):
        """Stopping a timer preserves elapsed time."""
        timer = Timer(
            id=uuid4(),
            duration=100,
            elapsed_time=45,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        paused_timer = timer.model_copy(update={"status": TimerStatus.paused})
        mock_repo.get_by_id.return_value = timer
        mock_repo.update.return_value = paused_timer
        result = await timer_service.stop_timer(timer.id)
        mock_repo.update.assert_called_once()
        call_kwargs = mock_repo.update.call_args[1]
        assert call_kwargs["elapsed_time"] == 45


class TestResetTimer:
    """Test resetting a timer."""

    @pytest.mark.asyncio
    async def test_reset_timer_clears_elapsed_time(self, timer_service, mock_repo, sample_timer):
        """Resetting a timer clears elapsed_time to 0."""
        running_timer = sample_timer.model_copy(
            update={"status": TimerStatus.running, "elapsed_time": 30}
        )
        reset_timer = running_timer.model_copy(
            update={"status": TimerStatus.idle, "elapsed_time": 0, "urgency_level": 0}
        )
        mock_repo.get_by_id.return_value = running_timer
        mock_repo.update.return_value = reset_timer
        result = await timer_service.reset_timer(running_timer.id)
        assert result.elapsed_time == 0
        assert result.status == TimerStatus.idle
        assert result.urgency_level == 0

    @pytest.mark.asyncio
    async def test_reset_timer_returns_none_if_not_found(self, timer_service, mock_repo):
        """Resetting a non-existent timer returns None."""
        mock_repo.get_by_id.return_value = None
        result = await timer_service.reset_timer(uuid4())
        assert result is None


class TestTickTimer:
    """Test timer tick (increment elapsed time by 1 second)."""

    @pytest.mark.asyncio
    async def test_tick_timer_increments_elapsed_time(self, timer_service, mock_repo, sample_timer):
        """Ticking a timer increments elapsed_time by 1."""
        ticked_timer = sample_timer.model_copy(update={"elapsed_time": 1})
        mock_repo.get_by_id.return_value = sample_timer
        mock_repo.update.return_value = ticked_timer
        result = await timer_service.tick_timer(sample_timer.id)
        mock_repo.update.assert_called_once()
        call_kwargs = mock_repo.update.call_args[1]
        assert call_kwargs["elapsed_time"] == 1

    @pytest.mark.asyncio
    async def test_tick_timer_updates_urgency(self, timer_service, mock_repo):
        """Ticking a timer updates urgency level based on new elapsed time."""
        timer = Timer(
            id=uuid4(),
            duration=100,
            elapsed_time=33,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        ticked_timer = timer.model_copy(update={"elapsed_time": 34, "urgency_level": 1})
        mock_repo.get_by_id.return_value = timer
        mock_repo.update.return_value = ticked_timer
        result = await timer_service.tick_timer(timer.id)
        assert result.urgency_level == 1

    @pytest.mark.asyncio
    async def test_tick_timer_marks_complete_at_duration(self, timer_service, mock_repo):
        """Ticking a timer to or past duration marks it complete."""
        timer = Timer(
            id=uuid4(),
            duration=60,
            elapsed_time=59,
            status=TimerStatus.running,
            urgency_level=3,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        complete_timer = timer.model_copy(
            update={"elapsed_time": 60, "status": TimerStatus.complete}
        )
        mock_repo.get_by_id.return_value = timer
        mock_repo.update.return_value = complete_timer
        result = await timer_service.tick_timer(timer.id)
        assert result.status == TimerStatus.complete

    @pytest.mark.asyncio
    async def test_tick_timer_returns_none_if_not_found(self, timer_service, mock_repo):
        """Ticking a non-existent timer returns None."""
        mock_repo.get_by_id.return_value = None
        result = await timer_service.tick_timer(uuid4())
        assert result is None


class TestListTimers:
    """Test listing all timers."""

    @pytest.mark.asyncio
    async def test_list_timers_returns_all(self, timer_service, mock_repo, sample_timer):
        """Listing timers returns all timers from repo."""
        timers = [sample_timer, sample_timer.model_copy(update={"id": uuid4()})]
        mock_repo.list_all.return_value = timers
        result = await timer_service.list_timers()
        assert len(result) == 2
        mock_repo.list_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_timers_returns_empty_list(self, timer_service, mock_repo):
        """Listing timers returns empty list when no timers exist."""
        mock_repo.list_all.return_value = []
        result = await timer_service.list_timers()
        assert result == []
