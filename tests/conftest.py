import asyncio
from typing import AsyncGenerator

import asyncpg
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.config import get_settings
from app.database import init_db
from app.main import create_app


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    """Create event loop for session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db_pool() -> AsyncGenerator[asyncpg.Pool, None]:
    """Create and tear down test database pool."""
    settings = get_settings()
    pool = await asyncpg.create_pool(
        settings.database_url,
        min_size=1,
        max_size=5,
    )
    
    await init_db(pool)
    
    yield pool
    
    async with pool.acquire() as conn:
        await conn.execute("TRUNCATE TABLE timers RESTART IDENTITY")
    
    await pool.close()


@pytest.fixture
async def async_client(test_db_pool: asyncpg.Pool) -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client with test database."""
    app = create_app()
    
    async def override_get_pool():
        return test_db_pool
    
    from app.main import get_pool
    app.dependency_overrides[get_pool] = override_get_pool
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
def client(async_client: AsyncClient) -> TestClient:
    """Synchronous test client for convenience."""
    return TestClient(async_client.app)
