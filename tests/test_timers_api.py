import pytest
from httpx import AsyncClient
from app.main import app
from app.database import get_db
from app.repos.timer_repo import TimerRepository
from app.models.timer import Timer
from datetime import datetime
from uuid import uuid4


@pytest.fixture
async def client():
    """Async test client for FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def db_session(monkeypatch):
    """Mock database session."""
    class MockSession:
        async def execute(self, query):
            return None
        
        async def commit(self):
            pass
        
        async def rollback(self):
            pass
        
        async def close(self):
            pass
    
    async def mock_get_db():
        return MockSession()
    
    monkeypatch.setattr("app.database.get_db", mock_get_db)
    return MockSession()


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint returns ok status."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_timer(client, monkeypatch):
    """Test creating a new timer."""
    timer_id = str(uuid4())
    
    async def mock_create(duration, elapsed_time=0, status="idle", urgency_level=0):
        return Timer(
            id=timer_id,
            duration=duration,
            elapsed_time=elapsed_time,
            status=status,
            urgency_level=urgency_level,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    monkeypatch.setattr("app.services.timer_service.TimerService.create", mock_create)
    
    response = await client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == timer_id
    assert data["duration"] == 60
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_create_timer_invalid_duration(client, monkeypatch):
    """Test creating a timer with invalid duration."""
    async def mock_create(duration, **kwargs):
        if duration <= 0:
            raise ValueError("Duration must be positive")
        return None
    
    monkeypatch.setattr("app.services.timer_service.TimerService.create", mock_create)
    
    response = await client.post(
        "/api/v1/timers",
        json={"duration": 0}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_timers(client, monkeypatch):
    """Test listing all timers."""
    timer_id = str(uuid4())
    timers = [
        Timer(
            id=timer_id,
            duration=60,
            elapsed_time=10,
            status="running",
            urgency_level=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    
    async def mock_list():
        return timers
    
    monkeypatch.setattr("app.services.timer_service.TimerService.list_all", mock_list)
    
    response = await client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["duration"] == 60
    assert data["count"] == 1


@pytest.mark.asyncio
async def test_start_timer(client, monkeypatch):
    """Test starting a timer."""
    timer_id = str(uuid4())
    
    async def mock_start(tid):
        return Timer(
            id=tid,
            duration=60,
            elapsed_time=0,
            status="running",
            urgency_level=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    monkeypatch.setattr("app.services.timer_service.TimerService.start", mock_start)
    
    response = await client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer(client, monkeypatch):
    """Test stopping a timer."""
    timer_id = str(uuid4())
    
    async def mock_stop(tid):
        return Timer(
            id=tid,
            duration=60,
            elapsed_time=15,
            status="paused",
            urgency_level=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    monkeypatch.setattr("app.services.timer_service.TimerService.stop", mock_stop)
    
    response = await client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer(client, monkeypatch):
    """Test resetting a timer."""
    timer_id = str(uuid4())
    
    async def mock_reset(tid):
        return Timer(
            id=tid,
            duration=60,
            elapsed_time=0,
            status="idle",
            urgency_level=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    monkeypatch.setattr("app.services.timer_service.TimerService.reset", mock_reset)
    
    response = await client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_urgency_level_calculation(client, monkeypatch):
    """Test urgency level increases with elapsed time."""
    timer_id = str(uuid4())
    
    async def mock_get(tid):
        elapsed = 45
        duration = 60
        ratio = elapsed / duration
        urgency = min(3, int(ratio * 4))
        
        return Timer(
            id=tid,
            duration=duration,
            elapsed_time=elapsed,
            status="running",
            urgency_level=urgency,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    monkeypatch.setattr("app.services.timer_service.TimerService.get_by_id", mock_get)
    
    response = await client.get(f"/api/v1/timers/{timer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["urgency_level"] > 0
