import pytest
from httpx import AsyncClient
from uuid import uuid4

from app.main import create_app


@pytest.mark.asyncio
async def test_health_check():
    """Health check endpoint returns ok status."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_timer():
    """Create a new timer with positive duration."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
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
async def test_create_timer_invalid_duration():
    """Create timer with invalid duration returns 400."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/timers",
            json={"duration": 0}
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data


@pytest.mark.asyncio
async def test_create_timer_negative_duration():
    """Create timer with negative duration returns 400."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/timers",
            json={"duration": -10}
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data


@pytest.mark.asyncio
async def test_list_timers():
    """List all timers returns array of timers."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/api/v1/timers", json={"duration": 60})
        await client.post("/api/v1/timers", json={"duration": 120})
        
        response = await client.get("/api/v1/timers")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "count" in data
        assert data["count"] >= 2


@pytest.mark.asyncio
async def test_start_timer():
    """Start a timer changes status to running."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
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
async def test_stop_timer():
    """Stop a timer changes status to paused."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
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
async def test_reset_timer():
    """Reset a timer resets elapsed_time to 0."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
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
async def test_update_timer_duration():
    """Update timer duration."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
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
async def test_timer_not_found():
    """Get non-existent timer returns 404."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        fake_id = str(uuid4())
        response = await client.post(f"/api/v1/timers/{fake_id}/start")
        assert response.status_code == 404
