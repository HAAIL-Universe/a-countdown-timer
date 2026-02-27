import pytest
from httpx import AsyncClient
from uuid import uuid4
from datetime import datetime

from app.main import app
from app.database import db
from app.models.timer import TimerStatus


@pytest.fixture
async def client():
    """Async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
async def setup_db():
    """Setup and teardown database for each test."""
    await db.connect()
    await db.execute("DELETE FROM timers")
    yield
    await db.execute("DELETE FROM timers")
    await db.disconnect()


@pytest.mark.asyncio
async def test_health_check(client):
    """Health check endpoint returns ok."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_timer(client):
    """Create a timer with initial duration."""
    response = await client.post(
        "/api/v1/timers",
        json={"duration": 60}
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
    """Create timer with invalid duration returns 400."""
    response = await client.post(
        "/api/v1/timers",
        json={"duration": 0}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_timer_missing_duration(client):
    """Create timer without duration returns 400."""
    response = await client.post(
        "/api/v1/timers",
        json={}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_timers(client):
    """List all timers."""
    await client.post("/api/v1/timers", json={"duration": 60})
    await client.post("/api/v1/timers", json={"duration": 120})

    response = await client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "timers" in data
    assert len(data["timers"]) == 2


@pytest.mark.asyncio
async def test_list_timers_empty(client):
    """List timers when none exist."""
    response = await client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "timers" in data
    assert len(data["timers"]) == 0


@pytest.mark.asyncio
async def test_start_timer(client):
    """Start a timer."""
    create_response = await client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_response.json()["id"]

    response = await client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_start_nonexistent_timer(client):
    """Start a timer that doesn't exist returns 404."""
    fake_id = str(uuid4())
    response = await client.post(f"/api/v1/timers/{fake_id}/start")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_stop_timer(client):
    """Stop (pause) a running timer."""
    create_response = await client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_response.json()["id"]

    await client.post(f"/api/v1/timers/{timer_id}/start")
    response = await client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_stop_nonexistent_timer(client):
    """Stop a timer that doesn't exist returns 404."""
    fake_id = str(uuid4())
    response = await client.post(f"/api/v1/timers/{fake_id}/stop")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_reset_timer(client):
    """Reset a timer to zero elapsed time."""
    create_response = await client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_response.json()["id"]

    response = await client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_reset_nonexistent_timer(client):
    """Reset a timer that doesn't exist returns 404."""
    fake_id = str(uuid4())
    response = await client.post(f"/api/v1/timers/{fake_id}/reset")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_timer_duration(client):
    """Update a timer's duration."""
    create_response = await client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_response.json()["id"]

    response = await client.post(
        f"/api/v1/timers/{timer_id}",
        json={"duration": 120}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["duration"] == 120


@pytest.mark.asyncio
async def test_update_timer_invalid_duration(client):
    """Update timer with invalid duration returns 400."""
    create_response = await client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_response.json()["id"]

    response = await client.post(
        f"/api/v1/timers/{timer_id}",
        json={"duration": 0}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_nonexistent_timer(client):
    """Update a timer that doesn't exist returns 404."""
    fake_id = str(uuid4())
    response = await client.post(
        f"/api/v1/timers/{fake_id}",
        json={"duration": 120}
    )
    assert response.status_code == 404
