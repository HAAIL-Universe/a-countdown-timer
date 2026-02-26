import pytest
from httpx import AsyncClient
from app.main import create_app
from app.database import init_db, close_db


@pytest.fixture
async def client():
    """Create test client with in-memory database."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_timer(client):
    """Test creating a new timer."""
    response = await client.post(
        "/api/v1/timers",
        json={
            "duration": 60,
            "elapsed_time": 0,
            "status": "idle",
            "urgency_level": 0,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["duration"] == 60
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"
    assert data["urgency_level"] == 0


@pytest.mark.asyncio
async def test_create_timer_invalid_duration(client):
    """Test creating timer with invalid duration."""
    response = await client.post(
        "/api/v1/timers",
        json={
            "duration": -1,
            "elapsed_time": 0,
            "status": "idle",
            "urgency_level": 0,
        },
    )
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_list_timers(client):
    """Test listing all timers."""
    await client.post(
        "/api/v1/timers",
        json={
            "duration": 60,
            "elapsed_time": 0,
            "status": "idle",
            "urgency_level": 0,
        },
    )
    response = await client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "count" in data
    assert data["count"] >= 1


@pytest.mark.asyncio
async def test_start_timer(client):
    """Test starting a timer."""
    create_response = await client.post(
        "/api/v1/timers",
        json={
            "duration": 60,
            "elapsed_time": 0,
            "status": "idle",
            "urgency_level": 0,
        },
    )
    timer_id = create_response.json()["id"]
    response = await client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer(client):
    """Test stopping a timer."""
    create_response = await client.post(
        "/api/v1/timers",
        json={
            "duration": 60,
            "elapsed_time": 0,
            "status": "idle",
            "urgency_level": 0,
        },
    )
    timer_id = create_response.json()["id"]
    await client.post(f"/api/v1/timers/{timer_id}/start")
    response = await client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer(client):
    """Test resetting a timer."""
    create_response = await client.post(
        "/api/v1/timers",
        json={
            "duration": 60,
            "elapsed_time": 30,
            "status": "paused",
            "urgency_level": 0,
        },
    )
    timer_id = create_response.json()["id"]
    response = await client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_urgency_level_calculation(client):
    """Test urgency level changes with elapsed time."""
    response = await client.post(
        "/api/v1/timers",
        json={
            "duration": 100,
            "elapsed_time": 50,
            "status": "paused",
            "urgency_level": 1,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["urgency_level"] == 1


@pytest.mark.asyncio
async def test_timer_not_found(client):
    """Test accessing non-existent timer."""
    response = await client.get("/api/v1/timers/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
