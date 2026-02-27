import asyncio
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.config import get_settings
from app.database import DatabasePool
from app.main import create_app


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def app():
    """Create test app with database."""
    os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/countdown_timer_test"
    await DatabasePool.initialize()
    _app = create_app()
    yield _app
    await DatabasePool.close()


@pytest_asyncio.fixture
async def client(app) -> AsyncGenerator:
    """Create async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as _client:
        yield _client


@pytest.fixture
def settings():
    """Return test settings."""
    return get_settings()
