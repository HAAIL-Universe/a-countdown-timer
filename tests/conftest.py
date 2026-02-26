import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from app.config import get_settings
from app.database import db
from app.main import create_app


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def app():
    """Create FastAPI app for testing."""
    return create_app()


@pytest.fixture
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture
async def db_connection():
    """Initialize database connection for tests."""
    settings = get_settings()
    await db.connect()
    yield db
    await db.disconnect()


@pytest.fixture
async def cleanup_timers(db_connection):
    """Clean up timers table before and after each test."""
    await db_connection.execute("DELETE FROM timers")
    yield
    await db_connection.execute("DELETE FROM timers")
