import pytest
import pytest_asyncio
from httpx import AsyncClient
import asyncpg
from typing import AsyncGenerator

from app.main import app
from app.database import get_pool, set_pool
from app.config import get_settings


@pytest_asyncio.fixture
async def test_db_pool() -> AsyncGenerator[asyncpg.Pool, None]:
    """Create and yield a test database pool, then clean up."""
    settings = get_settings()
    test_db_url = settings.database_url.replace(
        settings.database_url.split("/")[-1],
        f"{settings.database_url.split('/')[-1]}_test"
    )
    
    pool = await asyncpg.create_pool(
        test_db_url,
        min_size=1,
        max_size=5,
        command_timeout=10,
    )
    
    set_pool(pool)
    
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS timers (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                duration INTEGER NOT NULL,
                elapsed_time INTEGER NOT NULL DEFAULT 0,
                status VARCHAR(255) NOT NULL DEFAULT 'idle',
                urgency_level INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
        """)
    
    yield pool
    
    async with pool.acquire() as conn:
        await conn.execute("DROP TABLE IF EXISTS timers")
    
    await pool.close()


@pytest_asyncio.fixture
async def async_client(test_db_pool: asyncpg.Pool) -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def anyio_backend():
    """Use asyncio backend for pytest-asyncio."""
    return "asyncio"
