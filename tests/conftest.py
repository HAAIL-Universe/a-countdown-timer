import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.database import get_db
from app.models.timer import Timer
from app.repos.timer_repo import TimerRepository


@pytest.fixture
async def test_db_engine():
    """Create test database engine."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Timer.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_db_session(test_db_engine):
    """Create test database session."""
    async_session = async_sessionmaker(
        test_db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.fixture
async def test_client(test_db_session):
    """Create test HTTP client with overridden dependencies."""
    async def override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
async def timer_repo(test_db_session):
    """Create timer repository for tests."""
    return TimerRepository(test_db_session)
</
