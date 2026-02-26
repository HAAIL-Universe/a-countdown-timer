import pytest
import asyncpg
from httpx import AsyncClient
from typing import AsyncGenerator

from app.main import create_app
from app.database import set_pool


@pytest.fixture
async def test_pool() -> AsyncGenerator[asyncpg.Pool, None]:
    """Create and teardown test database pool."""
    pool = await asyncpg.create_pool(
        "postgresql://postgres:postgres@localhost:5432/countdown_timer_test",
        min_size=1,
        max_size=5,
    )

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
        await conn.execute("DROP TABLE IF EXISTS timers CASCADE")

    await pool.close()


@pytest.fixture
async def client(test_pool: asyncpg.Pool) -> AsyncGenerator[AsyncClient, None]:
    """Create async test client with test database pool."""
    set_pool(test_pool)
    app = create_app()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def anyio_backend():
    """Use asyncio as the anyio backend for async tests."""
    return "asyncio"
