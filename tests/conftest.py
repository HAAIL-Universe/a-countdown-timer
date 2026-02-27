"""pytest fixtures for integration tests."""
import asyncio
import pytest
import pytest_asyncio
import asyncpg
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import get_pool, close_pool


@pytest.fixture(scope="session")
def event_loop():
    """Create a single event loop for the entire test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_pool():
    """Provide a database pool and clean the timers table between tests."""
    pool = await get_pool()
    yield pool
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM timers")


@pytest_asyncio.fixture
async def async_client(db_pool):
    """Provide an httpx AsyncClient against the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
