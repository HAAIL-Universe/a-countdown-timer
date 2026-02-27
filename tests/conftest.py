import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy import text

from app.main import create_app
from app.database import get_pool, create_pool, close_pool, execute_query
from app.config import get_settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db_pool():
    """Create and teardown a test database pool for the entire session."""
    settings = get_settings()
    await create_pool()
    yield get_pool()
    await close_pool()


@pytest.fixture(autouse=True)
async def reset_timers_table(test_db_pool):
    """Truncate timers table before each test."""
    pool = test_db_pool
    await execute_query("TRUNCATE TABLE timers")
    yield
    await execute_query("TRUNCATE TABLE timers")


@pytest.fixture
async def client():
    """Create an async test client for the FastAPI app."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
