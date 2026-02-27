import pytest
from uuid import UUID
from datetime import datetime
from unittest.mock import AsyncMock

from app.models.timer import Timer, TimerStatus
from app.services.timer_service import TimerService


@pytest.fixture
def timer_id() -> UUID:
    return UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def mock_timer_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def service(mock_timer_repo: AsyncMock) -> TimerService:
    return TimerService(repo=mock_timer_repo)


@pytest.fixture
def sample_timer(timer_id: UUID) -> Timer:
    return Timer(
        id=timer_id,
        duration=100,
        elapsed_time=0,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


class TestComputeUrgency:
    """Test TimerService.compute_urgency urgency level computation."""

    def test_compute_urgency_level_0_for_0_to_33_percent(self, service: TimerService):
        """Urgency level 0 when elapsed < 33% of duration."""
        assert service.compute_urgency(0, 100) == 0
        assert service.compute_urgency(32, 100) == 0
        assert service.compute_urgency(1, 100) == 0

    def test_compute_urgency_level_1_for_33_to_66_percent(self, service: TimerService):
        """Urgency level 1 when 33% <= elapsed < 66% of duration."""
        assert service.compute_urgency(33, 100) == 1
        assert service.compute_urgency(50, 100) == 1
        assert service.compute_urgency(65, 100) == 1

    def test_compute_urgency_level_2_for_66_to_90_percent(self, service: TimerService):
        """Urgency level 2 when 66% <= elapsed < 90% of duration."""
        assert service.compute_urgency(66, 100) == 2
        assert service.compute_urgency(75, 100) == 2
        assert service.compute_urgency(89, 100) == 2

    def test_compute_urgency_level_3_for_90_percent_or_more(self, service: TimerService):
        """Urgency level 3 when elapsed >= 90% of duration."""
        assert service.compute_urgency(90, 100) == 3
        assert service.compute_urgency(95, 100) == 3
        assert service.compute_urgency(100, 100) == 3

    def test_compute_urgency_zero_duration_returns_0(self, service: TimerService):
        """Urgency level 0 when duration is zero (edge case)."""
        assert service.compute_urgency(0, 0) == 0
        assert service.compute_urgency(100, 0) == 0


class TestCreateTimer:
    """Test TimerService.create_timer."""

    @pytest.mark.asyncio
    async def test_create_timer_sets_idle_status(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer):
        """create_timer delegates to repo and returns Timer with idle status and elapsed_time=0."""
        mock_timer_repo.create.return_value = sample_timer

        result = await service.create_timer(100)

        assert result is not None
        assert result.status == TimerStatus.idle
        assert result.elapsed_time == 0
        assert result.duration == 100
        mock_timer_repo.create.assert_called_once_with(100)


class TestStartTimer:
    """Test TimerService.start_timer."""

    @pytest.mark.asyncio
    async def test_start_timer_sets_running_status(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer, timer_id: UUID):
        """start_timer transitions idle timer to running and computes urgency."""
        mock_timer_repo.get_by_id.return_value = sample_timer
        running_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=0,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_timer_repo.update.return_value = running_timer

        result = await service.start_timer(timer_id)

        assert result.status == TimerStatus.running
        mock_timer_repo.get_by_id.assert_called_once_with(timer_id)
        mock_timer_repo.update.assert_called_once_with(timer_id, 0, TimerStatus.running, 0)

    @pytest.mark.asyncio
    async def test_start_timer_from_paused(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer, timer_id: UUID):
        """start_timer can transition paused timer to running."""
        paused_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=50,
            status=TimerStatus.paused,
            urgency_level=1,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_timer_repo.get_by_id.return_value = paused_timer
        running_timer = Timer(
            id=paused_timer.id,
            duration=paused_timer.duration,
            elapsed_time=paused_timer.elapsed_time,
            status=TimerStatus.running,
            urgency_level=paused_timer.urgency_level,
            created_at=paused_timer.created_at,
            updated_at=paused_timer.updated_at,
        )
        mock_timer_repo.update.return_value = running_timer

        result = await service.start_timer(timer_id)

        assert result.status == TimerStatus.running
        mock_timer_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_timer_not_idle_or_paused_returns_unchanged(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer, timer_id: UUID):
        """start_timer on running or complete timer returns it unchanged."""
        running_timer = Timer(
            id=sample_timer.id,
            duration=sample_timer.duration,
            elapsed_time=sample_timer.elapsed_time,
            status=TimerStatus.running,
            urgency_level=sample_timer.urgency_level,
            created_at=sample_timer.created_at,
            updated_at=sample_timer.updated_at,
        )
        mock_timer_repo.get_by_id.return_value = running_timer

        result = await service.start_timer(timer_id)

        assert result.status == TimerStatus.running
        mock_timer_repo.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_start_timer_nonexistent_returns_none(self, service: TimerService, mock_timer_repo: AsyncMock, timer_id: UUID):
        """start_timer on nonexistent timer returns None."""
        mock_timer_repo.get_by_id.return_value = None

        result = await service.start_timer(timer_id)

        assert result is None


class TestStopTimer:
    """Test TimerService.stop_timer."""

    @pytest.mark.asyncio
    async def test_stop_timer_sets_paused_status(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer, timer_id: UUID):
        """stop_timer transitions running timer to paused."""
        running_timer = Timer(
            id=sample_timer.id,
            duration=sample_timer.duration,
            elapsed_time=sample_timer.elapsed_time,
            status=TimerStatus.running,
            urgency_level=sample_timer.urgency_level,
            created_at=sample_timer.created_at,
            updated_at=sample_timer.updated_at,
        )
        mock_timer_repo.get_by_id.return_value = running_timer
        paused_timer = Timer(
            id=running_timer.id,
            duration=running_timer.duration,
            elapsed_time=running_timer.elapsed_time,
            status=TimerStatus.paused,
            urgency_level=running_timer.urgency_level,
            created_at=running_timer.created_at,
            updated_at=running_timer.updated_at,
        )
        mock_timer_repo.update.return_value = paused_timer

        result = await service.stop_timer(timer_id)

        assert result.status == TimerStatus.paused
        mock_timer_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_timer_not_running_returns_unchanged(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer, timer_id: UUID):
        """stop_timer on idle or paused timer returns it unchanged."""
        mock_timer_repo.get_by_id.return_value = sample_timer

        result = await service.stop_timer(timer_id)

        assert result.status == TimerStatus.idle
        mock_timer_repo.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_stop_timer_nonexistent_returns_none(self, service: TimerService, mock_timer_repo: AsyncMock, timer_id: UUID):
        """stop_timer on nonexistent timer returns None."""
        mock_timer_repo.get_by_id.return_value = None

        result = await service.stop_timer(timer_id)

        assert result is None


class TestResetTimer:
    """Test TimerService.reset_timer."""

    @pytest.mark.asyncio
    async def test_reset_timer_clears_elapsed_time(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer, timer_id: UUID):
        """reset_timer sets elapsed_time to 0 and status to idle."""
        running_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=75,
            status=TimerStatus.running,
            urgency_level=2,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_timer_repo.get_by_id.return_value = running_timer
        reset_timer = Timer(
            id=running_timer.id,
            duration=running_timer.duration,
            elapsed_time=0,
            status=TimerStatus.idle,
            urgency_level=0,
            created_at=running_timer.created_at,
            updated_at=running_timer.updated_at,
        )
        mock_timer_repo.update.return_value = reset_timer

        result = await service.reset_timer(timer_id)

        assert result.elapsed_time == 0
        assert result.status == TimerStatus.idle
        mock_timer_repo.update.assert_called_once_with(timer_id, 0, TimerStatus.idle, 0)

    @pytest.mark.asyncio
    async def test_reset_timer_nonexistent_returns_none(self, service: TimerService, mock_timer_repo: AsyncMock, timer_id: UUID):
        """reset_timer on nonexistent timer returns None."""
        mock_timer_repo.get_by_id.return_value = None

        result = await service.reset_timer(timer_id)

        assert result is None


class TestTickTimer:
    """Test TimerService.tick_timer."""

    @pytest.mark.asyncio
    async def test_tick_timer_increments_elapsed_time(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer, timer_id: UUID):
        """tick_timer increments elapsed_time by 1 when running."""
        running_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=10,
            status=TimerStatus.running,
            urgency_level=0,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_timer_repo.get_by_id.return_value = running_timer
        ticked_timer = Timer(
            id=running_timer.id,
            duration=running_timer.duration,
            elapsed_time=11,
            status=running_timer.status,
            urgency_level=running_timer.urgency_level,
            created_at=running_timer.created_at,
            updated_at=running_timer.updated_at,
        )
        mock_timer_repo.update.return_value = ticked_timer

        result = await service.tick_timer(timer_id)

        assert result.elapsed_time == 11
        assert result.status == TimerStatus.running
        mock_timer_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_tick_timer_marks_complete_when_elapsed_exceeds_duration(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer, timer_id: UUID):
        """tick_timer marks timer complete when elapsed_time >= duration."""
        running_timer = Timer(
            id=timer_id,
            duration=100,
            elapsed_time=99,
            status=TimerStatus.running,
            urgency_level=3,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_timer_repo.get_by_id.return_value = running_timer
        complete_timer = Timer(
            id=running_timer.id,
            duration=running_timer.duration,
            elapsed_time=100,
            status=TimerStatus.complete,
            urgency_level=running_timer.urgency_level,
            created_at=running_timer.created_at,
            updated_at=running_timer.updated_at,
        )
        mock_timer_repo.update.return_value = complete_timer

        result = await service.tick_timer(timer_id)

        assert result.elapsed_time == 100
        assert result.status == TimerStatus.complete
        mock_timer_repo.update.assert_called_once_with(timer_id, 100, TimerStatus.complete, 3)

    @pytest.mark.asyncio
    async def test_tick_timer_not_running_returns_unchanged(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer, timer_id: UUID):
        """tick_timer on paused or idle timer returns it unchanged."""
        mock_timer_repo.get_by_id.return_value = sample_timer

        result = await service.tick_timer(timer_id)

        assert result.elapsed_time == 0
        mock_timer_repo.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_tick_timer_nonexistent_returns_none(self, service: TimerService, mock_timer_repo: AsyncMock, timer_id: UUID):
        """tick_timer on nonexistent timer returns None."""
        mock_timer_repo.get_by_id.return_value = None

        result = await service.tick_timer(timer_id)

        assert result is None


class TestListTimers:
    """Test TimerService.list_timers."""

    @pytest.mark.asyncio
    async def test_list_timers_returns_all_timers(self, service: TimerService, mock_timer_repo: AsyncMock, sample_timer: Timer):
        """list_timers returns the full list from repo."""
        second_timer = Timer(
            id=UUID("99999999-9999-9999-9999-999999999999"),
            duration=sample_timer.duration,
            elapsed_time=sample_timer.elapsed_time,
            status=sample_timer.status,
            urgency_level=sample_timer.urgency_level,
            created_at=sample_timer.created_at,
            updated_at=sample_timer.updated_at,
        )
        timers = [sample_timer, second_timer]
        mock_timer_repo.list_all.return_value = timers

        result = await service.list_timers()

        assert len(result) == 2
        assert result[0].id == sample_timer.id
        mock_timer_repo.list_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_timers_empty(self, service: TimerService, mock_timer_repo: AsyncMock):
        """list_timers returns empty list when no timers exist."""
        mock_timer_repo.list_all.return_value = []

        result = await service.list_timers()

        assert result == []
