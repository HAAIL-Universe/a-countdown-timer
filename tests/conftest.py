import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

from app.models.timer import Timer, TimerStatus
from app.services.timer_service import TimerService


@pytest.fixture(scope="session")
def event_loop():
    """Single event loop for the entire test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_repo() -> AsyncMock:
    """Mock TimerRepo with async methods."""
    repo = AsyncMock()
    return repo


@pytest.fixture
def timer_service(mock_repo: AsyncMock) -> TimerService:
    """TimerService instance with mocked repository."""
    return TimerService(repo=mock_repo)


@pytest.fixture
def sample_timer() -> Timer:
    """Sample timer for test data."""
    timer_id = uuid4()
    return Timer(
        id=timer_id,
        duration=60,
        elapsed_time=0,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
