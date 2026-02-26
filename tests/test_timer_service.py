import pytest
from datetime import datetime
from uuid import UUID, uuid4
from unittest.mock import AsyncMock, MagicMock
from app.models.timer import Timer, TimerStatus
from app.services.timer_service import TimerService
from app.repos.timer_repo import TimerRepository


@pytest.fixture
def mock_repo():
    """Mock TimerRepository for service tests."""
    return AsyncMock(spec=TimerRepository)


@pytest.fixture
def timer_service(mock_repo):
    """Create TimerService with mocked repository."""
    return TimerService(mock_repo)


@pytest.fixture
def sample_timer():
    """Create a sample Timer instance for testing."""
    return Timer(
        id=uuid4(),
        duration=60,
        elapsed_time=0,
        status=TimerStatus.IDLE,
        urgency_level=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


class TestTimerServiceCreate:
    """Tests for create_timer method."""

    @pytest.mark.asyncio
    async def test_create_timer_valid_duration(self, timer_service, mock_repo):
        """Test creating a timer with valid positive duration."""
        duration = 60
        timer_id = uuid4()
        created_timer = Timer(
            id=timer_id,
            duration=duration,
            elapsed_time=0,
            status=TimerStatus.IDLE,
            urgency_level=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        mock_repo.create.return_value = created_timer

        result = await timer_service.create_timer(duration)

        assert result.id == timer_id
        assert result.duration == duration
        assert result.elapsed_time == 0
        assert result.status == TimerStatus.IDLE
        assert result.urgency_level == 0
        mock_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_timer_invalid_duration_zero(self, timer_service):
        """Test creating a timer with zero duration raises ValueError."""
        with pytest.raises(ValueError, match="duration must be a positive integer"):
            await timer_service.create_timer(0)

    @pytest.mark.asyncio
    async def test_create_timer_invalid_duration_negative(self, timer_service):
        """Test creating a timer with negative duration raises ValueError."""
        with pytest.raises(ValueError, match="duration must be a positive integer"):
            await timer_service.create_timer(-10)


class TestTimerServiceSetDuration:
    """Tests for set_duration method."""

    @pytest.mark.asyncio
    async def test_set_duration_valid(self, timer_service, mock_repo, sample_timer):
        """Test setting duration on existing timer."""
        mock_repo.get_by_id.return_value = sample_timer
        mock_repo.update.return_value = sample_timer

        result = await timer_service.set_duration(sample_timer.id, 120)

        assert result.duration == 120
        mock_repo.get_by_id.assert_called_once_with(sample_timer.id)
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_duration_timer_not_found(self, timer_service, mock_repo):
        """Test setting duration on non-existent timer raises ValueError."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match=f"Timer {timer_id} not found"):
            await timer_service.set_duration(timer_id, 60)

    @pytest.mark.asyncio
    async def test_set_duration_invalid_zero(self, timer_service, mock_repo, sample_timer):
        """Test setting zero duration raises ValueError."""
        mock_repo.get_by_id.return_value = sample_timer

        with pytest.raises(ValueError, match="duration must be a positive integer"):
            await timer_service.set_duration(sample_timer.id, 0)


class TestTimerServiceStartTimer:
    """Tests for start_timer method."""

    @pytest.mark.asyncio
    async def test_start_timer_idle(self, timer_service, mock_repo, sample_timer):
        """Test starting an idle timer."""
        mock_repo.get_by_id.return_value = sample_timer
        started_timer = sample_timer.model_copy(update={"status": TimerStatus.RUNNING})
        mock_repo.update.return_value = started_timer

        result = await timer_service.start_timer(sample_timer.id)

        assert result.status == TimerStatus.RUNNING
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_timer_not_found(self, timer_service, mock_repo):
        """Test starting non-existent timer raises ValueError."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match=f"Timer {timer_id} not found"):
            await timer_service.start_timer(timer_id)


class TestTimerServiceStopTimer:
    """Tests for stop_timer method."""

    @pytest.mark.asyncio
    async def test_stop_timer_running(self, timer_service, mock_repo):
        """Test pausing a running timer."""
        running_timer = Timer(
            id=uuid4(),
            duration=60,
            elapsed_time=30,
            status=TimerStatus.RUNNING,
            urgency_level=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_by_id.return_value = running_timer
        paused_timer = running_timer.model_copy(update={"status": TimerStatus.PAUSED})
        mock_repo.update.return_value = paused_timer

        result = await timer_service.stop_timer(running_timer.id)

        assert result.status == TimerStatus.PAUSED
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_timer_not_found(self, timer_service, mock_repo):
        """Test stopping non-existent timer raises ValueError."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match=f"Timer {timer_id} not found"):
            await timer_service.stop_timer(timer_id)


class TestTimerServiceResetTimer:
    """Tests for reset_timer method."""

    @pytest.mark.asyncio
    async def test_reset_timer_partial_elapsed(self, timer_service, mock_repo):
        """Test resetting a partially elapsed timer."""
        running_timer = Timer(
            id=uuid4(),
            duration=60,
            elapsed_time=30,
            status=TimerStatus.RUNNING,
            urgency_level=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_by_id.return_value = running_timer
        reset_timer = running_timer.model_copy(
            update={
                "elapsed_time": 0,
                "status": TimerStatus.IDLE,
                "urgency_level": 0,
            }
        )
        mock_repo.update.return_value = reset_timer

        result = await timer_service.reset_timer(running_timer.id)

        assert result.elapsed_time == 0
        assert result.status == TimerStatus.IDLE
        assert result.urgency_level == 0
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_reset_timer_not_found(self, timer_service, mock_repo):
        """Test resetting non-existent timer raises ValueError."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match=f"Timer {timer_id} not found"):
            await timer_service.reset_timer(timer_id)


class TestTimerServiceGetTimer:
    """Tests for get_timer method."""

    @pytest.mark.asyncio
    async def test_get_timer_found(self, timer_service, mock_repo, sample_timer):
        """Test retrieving existing timer."""
        mock_repo.get_by_id.return_value = sample_timer

        result = await timer_service.get_timer(sample_timer.id)

        assert result == sample_timer
        mock_repo.get_by_id.assert_called_once_with(sample_timer.id)

    @pytest.mark.asyncio
    async def test_get_timer_not_found(self, timer_service, mock_repo):
        """Test retrieving non-existent timer returns None."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        result = await timer_service.get_timer(timer_id)

        assert result is None
        mock_repo.get_by_id.assert_called_once_with(timer_id)


class TestTimerServiceListTimers:
    """Tests for list_timers method."""

    @pytest.mark.asyncio
    async def test_list_timers_empty(self, timer_service, mock_repo):
        """Test listing timers when none exist."""
        mock_repo.list_all.return_value = []

        result = await timer_service.list_timers()

        assert result == []
        mock_repo.list_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_timers_multiple(self, timer_service, mock_repo):
        """Test listing multiple timers."""
        timers = [
            Timer(
                id=uuid4(),
                duration=60,
                elapsed_time=0,
                status=TimerStatus.IDLE,
                urgency_level=0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            Timer(
                id=uuid4(),
                duration=120,
                elapsed_time=30,
                status=TimerStatus.RUNNING,
                urgency_level=1,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]
        mock_repo.list_all.return_value = timers

        result = await timer_service.list_timers()

        assert len(result) == 2
        assert result == timers
        mock_repo.list_all.assert_called_once()


class TestTimerServiceTickTimer:
    """Tests for tick_timer method."""

    @pytest.mark.asyncio
    async def test_tick_timer_running(self, timer_service, mock_repo):
        """Test incrementing elapsed time on running timer."""
        running_timer = Timer(
            id=uuid4(),
            duration=60,
            elapsed_time=29,
            status=TimerStatus.RUNNING,
            urgency_level=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_by_id.return_value = running_timer
        ticked_timer = running_timer.model_copy(
            update={"elapsed_time": 30, "urgency_level": 0}
        )
        mock_repo.update.return_value = ticked_timer

        result = await timer_service.tick_timer(running_timer.id)

        assert result.elapsed_time == 30
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_tick_timer_reaches_duration(self, timer_service, mock_repo):
        """Test tick timer completes when elapsed_time reaches duration."""
        running_timer = Timer(
            id=uuid4(),
            duration=60,
            elapsed_time=59,
            status=TimerStatus.RUNNING,
            urgency_level=3,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_by_id.return_value = running_timer
        completed_timer = running_timer.model_copy(
            update={
                "elapsed_time": 60,
                "status": TimerStatus.COMPLETE,
                "urgency_level": 3,
            }
        )
        mock_repo.update.return_value = completed_timer

        result = await timer_service.tick_timer(running_timer.id)

        assert result.elapsed_time == 60
        assert result.status == TimerStatus.COMPLETE
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_tick_timer_paused_no_increment(self, timer_service, mock_repo):
        """Test tick timer does not increment when paused."""
        paused_timer = Timer(
            id=uuid4(),
            duration=60,
            elapsed_time=30,
            status=TimerStatus.PAUSED,
            urgency_level=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_by_id.return_value = paused_timer

        result = await timer_service.tick_timer(paused_timer.id)

        assert result.elapsed_time == 30
        mock_repo.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_tick_timer_not_found(self, timer_service, mock_repo):
        """Test ticking non-existent timer raises ValueError."""
        timer_id = uuid4()
        mock_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match=f"Timer {timer_id} not found"):
            await timer_service.tick_timer(timer_id)


class TestTimerServiceUrgencyLevel:
    """Tests for urgency level computation."""

    def test_compute_urgency_level_idle(self, timer_service):
        """Test urgency level 0 when elapsed is 0–33%."""
        urgency = timer_service._compute_urgency_level(10, 60)
        assert urgency == 0

    def test_compute_urgency_level_anxious(self, timer_service):
        """Test urgency level 1 when elapsed is 33–66%."""
        urgency = timer_service._compute_urgency_level(40, 60)
        assert urgency == 1

    def test_compute_urgency_level_upset(self, timer_service):
        """Test urgency level 2 when elapsed is 66–90%."""
        urgency = timer_service._compute_urgency_level(50, 60)
        assert urgency == 2

    def test_compute_urgency_level_critical(self, timer_service):
        """Test urgency level 3 when elapsed is 90%+."""
        urgency = timer_service._compute_urgency_level(55, 60)
        assert urgency == 3

    def test_compute_urgency_level_zero_duration(self, timer_service):
        """Test urgency level 0 with zero duration."""
        urgency = timer_service._compute_urgency_level(10, 0)
        assert urgency == 0
