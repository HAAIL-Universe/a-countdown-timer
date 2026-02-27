import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.database import db
from app.main import app


@pytest.fixture
async def client():
    """Provide an async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def setup_db():
    """Set up and tear down test database."""
    await db.connect()
    yield
    await db.disconnect()


@pytest.fixture
async def clean_timers_table(setup_db):
    """Clear timers table before each test."""
    async with db.pool.acquire() as conn:
        await conn.execute(text("DELETE FROM timers"))
    yield
    async with db.pool.acquire() as conn:
        await conn.execute(text("DELETE FROM timers"))
</pre>
