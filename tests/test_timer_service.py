"""Unit tests for TimerService urgency computation and state transitions using a mock repo."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime
from app.models.timer import Timer, TimerStatus
from app.services.timer_service import TimerService


def make_timer(
    duration: int = 100,
    elapsed_time: int = 0,
    status: TimerStatus = TimerStatus.idle,
    urgency_level: int = 0,
) -> Timer:
    """Helper to create a Timer instance for testing."""
    return Timer(
        id=uuid4(),
        duration=duration,
        elapsed_time=elapsed_time,
        status=status,
        urgency_level=urgency_level,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


def make_service() -> tuple[TimerService, AsyncMock]:
    """Create a TimerService with a mock repo."""
    mock_repo = AsyncMock()
    service = TimerService(mock_repo)
    return service, mock_repo


class TestComputeUrgency:
    """Tests for TimerService.compute_urgency."""

    def test_zero_to_33_returns_0(self):
        service, _ = make_service()
        assert service.compute_urgency(0, 100) == 0
        assert service.compute_urgency(32, 100) == 0

    def test_33_to_66_returns_1(self):
        service, _ = make_service()
        assert service.compute_urgency(33, 100) == 1
        assert service.compute_urgency(65, 100) == 1

    def test_66_to_90_returns_2(self):
        service, _ = make_service()
        assert service.compute_urgency(66, 100) == 2
        assert service.compute_urgency(89, 100) == 2

    def test_90_plus_returns_3(self):
        service, _ = make_service()
        assert service.compute_urgency(90, 100) == 3
        assert service.compute_urgency(100, 100) == 3

    def test_zero_duration_returns_0(self):
        service, _ = make_service()
        assert service.compute_urgency(50, 0) == 0


class TestCreateTimer:
    """Tests for TimerService.create_timer."""

    @pytest.mark.asyncio
    async def test_create_timer_delegates_to_repo(self):
        service, mock_repo = make_service()
        expected = make_timer(duration=60)
        mock_repo.create.return_value = expected

        result = await service.create_timer(60)

        mock_repo.create.assert_called_once_with(60)
        assert result == expected


class TestStartTimer:
    """Tests for TimerService.start_timer."""

    @pytest.mark.asyncio
    async def test_start_timer_sets_running_status(self):
        service, mock_repo = make_service()
        timer = make_timer(duration=100, elapsed_time=0, status=TimerStatus.idle)
        mock_repo.get_by_id.return_value = timer
        mock_repo.update.return_value = make_timer(
            duration=100, elapsed_time=0, status=TimerStatus.running
        )

        result = await service.start_timer(timer.id)

        mock_repo.update.assert_called_once()
        call_kwargs = mock_repo.update.call_args
        assert call_kwargs[1]['status'] == TimerStatus.running

    @pytest.mark.asyncio
    async def test_start_timer_returns_none_if_not_found(self):
        service, mock_repo = make_service()
        mock_repo.get_by_id.return_value = None

        result = await service.start_timer(uuid4())

        assert result is None


class TestStopTimer:
    """Tests for TimerService.stop_timer."""

    @pytest.mark.asyncio
    async def test_stop_timer_sets_paused_status(self):
        service, mock_repo = make_service()
        timer = make_timer(duration=100, elapsed_time=30, status=TimerStatus.running)
        mock_repo.get_by_id.return_value = timer
        mock_repo.update.return_value = make_timer(
            duration=100, elapsed_time=30, status=TimerStatus.paused
        )

        result = await service.stop_timer(timer.id)

        call_kwargs = mock_repo.update.call_args
        assert call_kwargs[1]['status'] == TimerStatus.paused


class TestResetTimer:
    """Tests for TimerService.reset_timer."""

    @pytest.mark.asyncio
    async def test_reset_timer_clears_elapsed_time(self):
        service, mock_repo = make_service()
        timer = make_timer(duration=100, elapsed_time=50, status=TimerStatus.paused)
        mock_repo.get_by_id.return_value = timer
        mock_repo.update.return_value = make_timer(
            duration=100, elapsed_time=0, status=TimerStatus.idle, urgency_level=0
        )

        result = await service.reset_timer(timer.id)

        call_kwargs = mock_repo.update.call_args
        assert call_kwargs[1]['elapsed_time'] == 0
        assert call_kwargs[1]['status'] == TimerStatus.idle
        assert call_kwargs[1]['urgency_level'] == 0
