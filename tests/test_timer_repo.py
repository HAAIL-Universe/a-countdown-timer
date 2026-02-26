import asyncio
import pytest
import asyncpg
from uuid import UUID
from datetime import datetime

from app.config import DATABASE_URL
from app.models.timer import Timer, TimerStatus


class TimerRepo:
    """Repository for Timer database operations."""
    
    def __init__(self, pool):
        self.pool = pool
    
    async def create(self, duration: int) -> Timer:
        """Create a new timer."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO timers (duration, elapsed_time, status, urgency_level, created_at, updated_at)
                VALUES ($1, $2, $3, $4, NOW(), NOW())
                RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
                """,
                duration, 0, TimerStatus.IDLE.value, 0
            )
        return Timer(
            id=row['id'],
            duration=row['duration'],
            elapsed_time=row['elapsed_time'],
            status=TimerStatus(row['status']),
            urgency_level=row['urgency_level'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
    async def get_by_id(self, timer_id: UUID) -> Timer | None:
        """Retrieve timer by ID."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, duration, elapsed_time, status, urgency_level, created_at, updated_at FROM timers WHERE id = $1",
                timer_id
            )
        if row is None:
            return None
        return Timer(
            id=row['id'],
            duration=row['duration'],
            elapsed_time=row['elapsed_time'],
            status=TimerStatus(row['status']),
            urgency_level=row['urgency_level'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
    async def update(self, timer_id: UUID, elapsed_time: int, status: TimerStatus, urgency_level: int) -> Timer | None:
        """Update timer."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                UPDATE timers
                SET elapsed_time = $2, status = $3, urgency_level = $4, updated_at = NOW()
                WHERE id = $1
                RETURNING id, duration, elapsed_time, status, urgency_level, created_at, updated_at
                """,
                timer_id, elapsed_time, status.value, urgency_level
            )
        if row is None:
            return None
        return Timer(
            id=row['id'],
            duration=row['duration'],
            elapsed_time=row['elapsed_time'],
            status=TimerStatus(row['status']),
            urgency_level=row['urgency_level'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )


@pytest.fixture(scope="session")
def event_loop():
    """Session-scoped event loop for async tests."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
async def db_pool():
    """Create and tear down asyncpg pool for tests."""
    pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=1,
        max_size=5,
        max_queries=50000,
        max_inactive_connection_lifetime=300.0,
    )
    yield pool
    await pool.close()


@pytest.fixture
async def repo(db_pool):
    """Instantiate TimerRepo with test pool."""
    return TimerRepo(db_pool)


@pytest.fixture
async def clean_db(db_pool):
    """Truncate timers table before each test."""
    async with db_pool.acquire() as conn:
        await conn.execute("TRUNCATE timers CASCADE")
    yield
    async with db_pool.acquire() as conn:
        await conn.execute("TRUNCATE timers CASCADE")


@pytest.mark.asyncio
async def test_create_timer(repo, clean_db):
    """TimerRepo.create returns Timer with correct duration, IDLE status, 0 elapsed_time."""
    timer = await repo.create(duration=60)
    
    assert timer.id is not None
    assert isinstance(timer.id, UUID)
    assert timer.duration == 60
    assert timer.elapsed_time == 0
    assert timer.status == TimerStatus.IDLE
    assert timer.urgency_level == 0
    assert timer.created_at is not None
    assert timer.updated_at is not None


@pytest.mark.asyncio
async def test_create_timer_stores_in_db(repo, clean_db, db_pool):
    """Created timer persists in database."""
    timer = await repo.create(duration=120)
    
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM timers WHERE id = $1", timer.id)
    
    assert row is not None
    assert int(row["duration"]) == 120
    assert int(row["elapsed_time"]) == 0
    assert row["status"] == "IDLE"


@pytest.mark.asyncio
async def test_get_nonexistent_timer(repo, clean_db):
    """TimerRepo.get_by_id returns None for unknown UUIDs."""
    from uuid import uuid4
    
    result = await repo.get_by_id(uuid4())
    assert result is None


@pytest.mark.asyncio
async def test_get_timer_by_id(repo, clean_db):
    """TimerRepo.get_by_id retrieves created timer."""
    created = await repo.create(duration=45)
    
    retrieved = await repo.get_by_id(created.id)
    
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.duration == 45
    assert retrieved.elapsed_time == 0
    assert retrieved.status == TimerStatus.IDLE


@pytest.mark.asyncio
async def test_update_timer(repo, clean_db):
    """TimerRepo.update persists status, elapsed_time, and urgency_level changes."""
    timer = await repo.create(duration=100)
    
    updated = await repo.update(
        timer_id=timer.id,
        elapsed_time=50,
        status=TimerStatus.RUNNING,
        urgency_level=1
    )
    
    assert updated is not None
    assert updated.id == timer.id
    assert updated.elapsed_time == 50
    assert updated.status == TimerStatus.RUNNING
    assert updated.urgency_level == 1


@pytest.mark.asyncio
async def test_update_timer_persists(repo, clean_db):
    """Updated timer changes persist in database."""
    timer = await repo.create(duration=75)
    
    await repo.update(
        timer_id=timer.id,
        elapsed_time=30,
        status=TimerStatus.PAUSED,
        urgency_level=0
    )
    
    retrieved = await repo.get_by_id(timer.id)
    
    assert retrieved is not None
    assert retrieved.elapsed_time == 30
    assert retrieved.status == TimerStatus.PAUSED


@pytest.mark.asyncio
async def test_update_nonexistent_timer(repo, clean_db):
    """TimerRepo.update returns None for unknown timer."""
    from uuid import uuid4
    
    result = await repo.update(
        timer_id=uuid4(),
        elapsed_time=10,
        status=TimerStatus.RUNNING,
        urgency_level=1
    )
    
    assert result is None
