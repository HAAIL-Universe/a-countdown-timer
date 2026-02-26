import pytest
import asyncio
from unittest.mock import AsyncMock
from uuid import uuid4
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
    """Mock TimerRepo with async methods."""
    repo = AsyncMock()
    return repo


@pytest.fixture
def sample_timer() -> Timer:
    """Sample Timer instance for testing."""
    timer_id = uuid4()
    return Timer(
        id=timer_id,
        duration=100,
        elapsed_time=50,
        status=TimerStatus.idle,
        urgency_level=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
