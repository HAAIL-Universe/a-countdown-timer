import os
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.database import Database, get_db


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """Set environment variables for testing before app imports."""
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@localhost:5432/countdown_timer_test"
    os.environ["CORS_ORIGINS"] = "http://localhost:3000,http://localhost:5173"


@pytest.fixture
async def db() -> AsyncGenerator[Database, None]:
    """Provide test database connection."""
    db = Database("postgresql+asyncpg://postgres:postgres@localhost:5432/countdown_timer_test")
    await db.connect()
    yield db
    await db.disconnect()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provide async test client for API."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def async_session_maker():
    """Provide async session factory for tests."""
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/countdown_timer_test",
        echo=False,
    )
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    yield async_session
    await engine.dispose()
</
