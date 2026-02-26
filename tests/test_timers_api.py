import pytest
from httpx import AsyncClient
from uuid import uuid4

from app.main import app
from app.database import db
from app.models import Timer


@pytest.fixture
async def client():
    """Provide async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def setup_db():
    """Setup and teardown database for tests."""
    await db.connect()
    await db.execute("TRUNCATE timers RESTART IDENTITY CASCADE;")
    yield
    await db.execute("TRUNCATE timers RESTART IDENTITY CASCADE;")
    await db.disconnect()


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_timer(client: AsyncClient, setup_db):
    """Test creating a new timer."""
    payload = {
        "duration": 60,
        "elapsed_time": 0,
        "status": "idle",
        "urgency_level": 0,
    }
    response = await client.post("/api/v1/timers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["message"] == "Created"


@pytest.mark.asyncio
async def test_create_timer_invalid_duration(client: AsyncClient, setup_db):
    """Test creating a timer with invalid duration."""
    payload = {
        "duration": -10,
        "elapsed_time": 0,
        "status": "idle",
        "urgency_level": 0,
    }
    response = await client.post("/api/v1/timers", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_get_timers(client: AsyncClient, setup_db):
    """Test listing all timers."""
    payload = {
        "duration": 60,
        "elapsed_time": 0,
        "status": "idle",
        "urgency_level": 0,
    }
    await client.post("/api/v1/timers", json=payload)
    await client.post("/api/v1/timers", json=payload)

    response = await client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "count" in data
    assert data["count"] == 2


@pytest.mark.asyncio
async def test_start_timer(client: AsyncClient, setup_db):
    """Test starting a timer."""
    create_payload = {
        "duration": 60,
        "elapsed_time": 0,
        "status": "idle",
        "urgency_level": 0,
    }
    create_response = await client.post("/api/v1/timers", json=create_payload)
    timer_id = create_response.json()["id"]

    response = await client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer(client: AsyncClient, setup_db):
    """Test stopping a timer."""
    create_payload = {
        "duration": 60,
        "elapsed_time": 0,
        "status": "idle",
        "urgency_level": 0,
    }
    create_response = await client.post("/api/v1/timers", json=create_payload)
    timer_id = create_response.json()["id"]

    await client.post(f"/api/v1/timers/{timer_id}/start")
    response = await client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer(client: AsyncClient, setup_db):
    """Test resetting a timer."""
    create_payload = {
        "duration": 60,
        "elapsed_time": 30,
        "status": "paused",
        "urgency_level": 1,
    }
    create_response = await client.post("/api/v1/timers", json=create_payload)
    timer_id = create_response.json()["id"]

    response = await client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_update_timer_duration(client: AsyncClient, setup_db):
    """Test updating timer duration."""
    create_payload = {
        "duration": 60,
        "elapsed_time": 0,
        "status": "idle",
        "urgency_level": 0,
    }
    create_response = await client.post("/api/v1/timers", json=create_payload)
    timer_id = create_response.json()["id"]

    update_payload = {"duration": 120}
    response = await client.post(f"/api/v1/timers/{timer_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["duration"] == 120


@pytest.mark.asyncio
async def test_timer_urgency_level_low(client: AsyncClient, setup_db):
    """Test urgency level computation at low elapsed time."""
    payload = {
        "duration": 100,
        "elapsed_time": 10,
        "status": "running",
        "urgency_level": 0,
    }
    response = await client.post("/api/v1/timers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["urgency_level"] == 0


@pytest.mark.asyncio
async def test_timer_urgency_level_medium(client: AsyncClient, setup_db):
    """Test urgency level computation at medium elapsed time."""
    payload = {
        "duration": 100,
        "elapsed_time": 50,
        "status": "running",
        "urgency_level": 0,
    }
    response = await client.post("/api/v1/timers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["urgency_level"] == 1


@pytest.mark.asyncio
async def test_timer_urgency_level_high(client: AsyncClient, setup_db):
    """Test urgency level computation at high elapsed time."""
    payload = {
        "duration": 100,
        "elapsed_time": 80,
        "status": "running",
        "urgency_level": 0,
    }
    response = await client.post("/api/v1/timers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["urgency_level"] == 2


@pytest.mark.asyncio
async def test_timer_not_found(client: AsyncClient, setup_db):
    """Test accessing non-existent timer."""
    fake_id = str(uuid4())
    response = await client.get(f"/api/v1/timers/{fake_id}")
    assert response.status_code == 404
