import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient

from app.main import app
from app.database import Database


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Set test environment variables before importing config."""
    os.environ.setdefault("DATABASE_URL", "postgresql://localhost/countdown_timer_test")
    os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
    yield
    if "DATABASE_URL" in os.environ and "test" in os.environ["DATABASE_URL"]:
        del os.environ["DATABASE_URL"]
    if "CORS_ORIGINS" in os.environ:
        del os.environ["CORS_ORIGINS"]


@pytest.fixture
async def db_mock() -> AsyncMock:
    """Provide a mocked Database instance."""
    mock_db = AsyncMock(spec=Database)
    mock_db.pool = MagicMock()
    return mock_db


@pytest.fixture
async def client() -> AsyncClient:
    """Provide an async HTTP client for testing the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_database(db_mock):
    """Patch the database module with a mock."""
    with patch("app.database.db", db_mock):
        yield db_mock
