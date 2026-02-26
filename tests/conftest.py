import pytest
from httpx import AsyncClient
from app.main import create_app
from app.database import init_db, cleanup_db


@pytest.fixture
async def client():
    """Provide an async HTTP client for testing."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_db():
    """Initialize database before each test."""
    await init_db()
    yield
    await cleanup_db()
