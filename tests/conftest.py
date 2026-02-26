import pytest
import asyncio
from unittest.mock import AsyncMock
from uuid import UUID, uuid4
from datetime import datetime
from app.models.timer import Timer, TimerStatus


@pytest.fixture(scope="session")
def event_loop():
    """Single event loop for the entire test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_repo() -> AsyncMock:
    """Mock repository for TimerService tests."""
    return AsyncMock()


@pytest.fixture
def sample_timer_id() -> UUID:
    """A consistent timer ID for tests."""
    return uuid4()


@pytest.fixture
def sample_timer(sample_timer_id: UUID) -> Timer:
    """A sample timer in idle state."""
    return Timer(
        id=sample_timer_id,
        duration=100,
        elapsed_time=0,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
