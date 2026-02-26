import pytest
from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from app.models.timer import Timer, TimerStatus
from app.services.timer_service import TimerService


@pytest.fixture
def mock_repo():
    """Create a mock repository."""
    return AsyncMock()


@pytest.fixture
def timer_service(mock_repo):
    """Create a TimerService with mocked repository."""
    return TimerService(mock_repo)


@pytest.fixture
def sample_timer_dict():
    """Create a sample timer dictionary."""
    return {
        "id": uuid4(),
        "duration": 60,
        "elapsed_time": 0,
        "status": "idle",
        "urgency_level": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


class TestComputeUrgencyLevel:
    """Test urgency level computation."""

    def test_urgency_level_happy_0_to_33_percent(self, timer_service):
        """Urgency level 0 when elapsed time is 0-33% of duration."""
        assert timer_service._compute_urgency_level(10, 100) == 0
        assert timer_service._compute_urgency_level(33, 100) == 0

    def test_urgency_level_anxious_33_to_66_percent(self, timer_service):
        """Urgency level 1 when elapsed time is 33-66% of duration."""
        assert timer_service._compute_urgency_level(34, 100) == 1
        assert timer_service._compute_urgency_level(65, 100) == 1

    def test_urgency_level_upset_66_to_90_percent(self, timer_service):
        """Urgency level 2 when elapsed time is 66-90% of duration."""
        assert timer_service._compute_urgency_level(66, 100) == 2
        assert timer_service._compute_urgency_level(89, 100) == 2

    def test_urgency_level_critical_90_plus_percent(self, timer_service):
        """Urgency level 3 when elapsed time is 90%+ of duration."""
        assert timer_service._compute_urgency_level(90, 100) == 3
        assert timer_service._compute_urgency_level(99, 100) == 3

    def test_urgency_level_zero_duration(self, timer_service):
        """Urgency level 0 when duration is zero or negative."""
        assert timer_service._compute_urgency_level(10, 0) == 0
        assert timer_service._compute_urgency_level(10, -5) == 0


class TestCreateTimer:
    """Test timer creation."""

    @pytest.mark.asyncio
    async def test_create_timer_success(self, timer_service, mock_repo, sample_timer_dict):
        """Successfully create a new timer."""
        mock_repo.create.return_value = sample_timer_dict

        result = await timer_service.create_timer(60)

        assert result.id == sample_timer_dict["id"]
        assert result.duration == 60
        assert result.elapsed_time == 0
        assert result.status == TimerStatus.IDLE
        assert result.urgency_level == 0
        mock_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_timer_invalid_duration(self, timer_service):
        """Raise error when duration is non-positive."""
        with pytest.raises(ValueError, match="Duration must be positive"):
            await timer_service.create_timer(0)

        with pytest.raises(ValueError, match="Duration must be positive"):
            await timer_service.create_timer(-10)


class TestGetTimer:
    """Test timer retrieval."""

    @pytest.mark.asyncio
    async def test_get_timer_success(self, timer_service, mock_repo, sample_timer_dict):
        """Successfully fetch a timer by ID."""
        timer_id = sample_timer_dict["id"]
        mock_repo.get_by_id.return_value = sample_timer_dict

        result = await timer_service.get_timer(timer_id)

        assert result is not None
        assert result.id == timer_id
        mock_repo.get_by_id.assert_called_once_with(timer_id)

    @pytest.mark.asyncio
    async def test_get_timer_not_found(self, timer_service, mock_repo):
        """Return None when timer is not found."""
        mock_repo.get_by_id.return_value = None
        timer_id = uuid4()

        result = await timer_service.get_timer(timer_id)

        assert result is None


class TestListTimers:
    """Test listing timers."""

    @pytest.mark.asyncio
    async def test_list_timers_success(self, timer_service, mock_repo, sample_timer_dict):
        """Successfully list all timers."""
        mock_repo.list_all.return_value = [sample_timer_dict, sample_timer_dict]

        result = await timer_service.list_timers()

        assert len(result) == 2
        assert all(isinstance(t, Timer) for t in result)
        mock_repo.list_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_timers_empty(self, timer_service, mock_repo):
        """Return empty list when no timers exist."""
        mock_repo.list_all.return_value = []

        result = await timer_service.list_timers()

        assert result == []


class TestSetDuration:
    """Test setting timer duration."""

    @pytest.mark.asyncio
    async def test_set_duration_success(self, timer_service, mock_repo, sample_timer_dict):
        """Successfully update timer duration."""
        timer_id = sample_timer_dict["id"]
        updated_dict = {**sample_timer_dict, "duration": 120}
        mock_repo.update.return_value = updated_dict

        result = await timer_service.set_duration(timer_id, 120)

        assert result is not None
        assert result.duration == 120
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_duration_invalid(self, timer_service):
        """Raise error when duration is non-positive."""
        with pytest.raises(ValueError, match="Duration must be positive"):
            await timer_service.set_duration(uuid4(), 0)

    @pytest.mark.asyncio
    async def test_set_duration_not_found(self, timer_service, mock_repo):
        """Return None when timer is not found."""
        mock_repo.update.return_value = None

        result = await timer_service.set_duration(uuid4(), 60)

        assert result is None


class TestStartTimer:
    """Test starting timer."""

    @pytest.mark.asyncio
    async def test_start_timer_success(self, timer_service, mock_repo, sample_timer_dict):
        """Successfully start a timer."""
        timer_id = sample_timer_dict["id"]
        running_dict = {**sample_timer_dict, "status": "running"}
        mock_repo.get_by_id.return_value = sample_timer_dict
        mock_repo.update.return_value = running_dict

        result = await timer_service.start_timer(timer_id)

        assert result is not None
        assert result.status == TimerStatus.RUNNING
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_timer_not_found(self, timer_service, mock_repo):
        """Return None when timer is not found."""
        mock_repo.get_by_id.return_value = None

        result = await timer_service.start_timer(uuid4())

        assert result is None


class TestStopTimer:
    """Test stopping (pausing) timer."""

    @pytest.mark.asyncio
    async def test_stop_timer_success(self, timer_service, mock_repo, sample_timer_dict):
        """Successfully pause a timer."""
        timer_id = sample_timer_dict["id"]
        paused_dict = {**sample_timer_dict, "status": "paused"}
        mock_repo.get_by_id.return_value = sample_timer_dict
        mock_repo.update.return_value = paused_dict

        result = await timer_service.stop_timer(timer_id)

        assert result is not None
        assert result.status == TimerStatus.PAUSED
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_timer_not_found(self, timer_service, mock_repo):
        """Return None when timer is not found."""
        mock_repo.get_by_id.return_value = None

        result = await timer_service.stop_timer(uuid4())

        assert result is None


class TestResetTimer:
    """Test resetting timer."""

    @pytest.mark.asyncio
    async def test_reset_timer_success(self, timer_service, mock_repo, sample_timer_dict):
        """Successfully reset a timer."""
        timer_id = sample_timer_dict["id"]
        reset_dict = {
            **sample_timer_dict,
            "elapsed_time": 0,
            "status": "idle",
            "urgency_level": 0,
        }
        mock_repo.get_by_id.return_value = sample_timer_dict
        mock_repo.update.return_value = reset_dict

        result = await timer_service.reset_timer(timer_id)

        assert result is not None
        assert result.elapsed_time == 0
        assert result.status == TimerStatus.IDLE
        assert result.urgency_level == 0
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_reset_timer_not_found(self, timer_service, mock_repo):
        """Return None when timer is not found."""
        mock_repo.get_by_id.return_value = None

        result = await timer_service.reset_timer(uuid4())

        assert result is None


class TestDictToTimer:
    """Test dictionary to Timer model conversion."""

    def test_dict_to_timer_success(self, timer_service, sample_timer_dict):
        """Successfully convert dict to Timer model."""
        result = timer_service._dict_to_timer(sample_timer_dict)

        assert result is not None
        assert isinstance(result, Timer)
        assert result.id == sample_timer_dict["id"]
        assert result.duration == sample_timer_dict["duration"]
        assert result.status == TimerStatus.IDLE

    def test_dict_to_timer_none(self, timer_service):
        """Return None when input is None."""
        result = timer_service._dict_to_timer(None)

        assert result is None
