import os
import pytest
from httpx import AsyncClient
from app.main import create_app
from app.database import Database, db as global_db


@pytest.fixture(scope="session")
def test_database_url():
    """Provide test database URL, defaulting to test DB if not set."""
    return os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost/countdown_timer_test")


@pytest.fixture(scope="session")
async def setup_test_db(test_database_url):
    """Set up test database schema."""
    test_db = Database(test_database_url)
    await test_db.connect()
    await test_db.init_schema()
    yield test_db
    await test_db.disconnect()


@pytest.fixture
async def app(setup_test_db, test_database_url, monkeypatch):
    """Create test FastAPI app with test database."""
    monkeypatch.setenv("DATABASE_URL", test_database_url)
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:5173")
    
    import app.config
    app.config.settings = app.config.Settings(
        database_url=test_database_url,
        cors_origins="http://localhost:5173"
    )
    
    import app.database
    app.database.db = setup_test_db
    
    test_app = create_app()
    yield test_app


@pytest.fixture
async def client(app):
    """Create async test HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
async def cleanup_db(setup_test_db):
    """Clean up database between tests."""
    yield
    await setup_test_db.execute("TRUNCATE TABLE timers RESTART IDENTITY;")
