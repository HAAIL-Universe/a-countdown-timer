import pytest
from httpx import AsyncClient
from uuid import UUID

from app.main import create_app


@pytest.fixture
async def client():
    """Provide async test client."""
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
    response = await client.post("/api/v1/timers", json={"duration": 300})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["duration"] == 300
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"
    assert data["urgency_level"] == 0
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_timer_invalid_duration(client):
    """Test creating a timer with invalid duration."""
    response = await client.post("/api/v1/timers", json={"duration": 0})
    assert response.status_code == 400
    assert "error" in response.json()


@pytest.mark.asyncio
async def test_list_timers(client):
    """Test listing all timers."""
    await client.post("/api/v1/timers", json={"duration": 300})
    response = await client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "count" in data
    assert isinstance(data["items"], list)
    assert isinstance(data["count"], int)


@pytest.mark.asyncio
async def test_get_timer(client):
    """Test getting a specific timer."""
    create_response = await client.post("/api/v1/timers", json={"duration": 300})
    timer_id = create_response.json()["id"]
    response = await client.get(f"/api/v1/timers/{timer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == timer_id
    assert data["duration"] == 300


@pytest.mark.asyncio
async def test_get_timer_not_found(client):
    """Test getting a non-existent timer."""
    response = await client.get(f"/api/v1/timers/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_start_timer(client):
    """Test starting a timer."""
    create_response = await client.post("/api/v1/timers", json={"duration": 300})
    timer_id = create_response.json()["id"]
    response = await client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer(client):
    """Test stopping a timer."""
    create_response = await client.post("/api/v1/timers", json={"duration": 300})
    timer_id = create_response.json()["id"]
    await client.post(f"/api/v1/timers/{timer_id}/start")
    response = await client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer(client):
    """Test resetting a timer."""
    create_response = await client.post("/api/v1/timers", json={"duration": 300})
    timer_id = create_response.json()["id"]
    response = await client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_update_timer_duration(client):
    """Test updating timer duration."""
    create_response = await client.post("/api/v1/timers", json={"duration": 300})
    timer_id = create_response.json()["id"]
    response = await client.post(f"/api/v1/timers/{timer_id}", json={"duration": 600})
    assert response.status_code == 200
    data = response.json()
    assert data["duration"] == 600


@pytest.mark.asyncio
async def test_urgency_level_calculation(client):
    """Test urgency level calculation based on elapsed time."""
    create_response = await client.post("/api/v1/timers", json={"duration": 100})
    timer_id = create_response.json()["id"]
    
    response = await client.get(f"/api/v1/timers/{timer_id}")
    assert response.json()["urgency_level"] == 0
