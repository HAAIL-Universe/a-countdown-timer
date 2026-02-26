import pytest
from httpx import AsyncClient
from uuid import UUID
from app.main import app
from app.models.timer import TimerStatus


@pytest.mark.asyncio
async def test_health_check():
    """Health check endpoint returns ok."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_timer():
    """Create a new timer with positive duration."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/timers", json={"duration": 60})
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["duration"] == 60
        assert data["elapsed_time"] == 0
        assert data["status"] == TimerStatus.IDLE.value
        assert data["urgency_level"] == 0
        assert UUID(data["id"])


@pytest.mark.asyncio
async def test_create_timer_invalid_duration():
    """Create timer with invalid duration returns 400."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/timers", json={"duration": 0})
        assert response.status_code == 400
        assert "error" in response.json()

        response = await client.post("/api/v1/timers", json={"duration": -10})
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_all_timers():
    """List all timers."""
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
async def test_get_timer_by_id():
    """Get a specific timer by ID."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_resp = await client.post("/api/v1/timers", json={"duration": 60})
        timer_id = create_resp.json()["id"]
        
        response = await client.get(f"/api/v1/timers/{timer_id}")
        assert response.status_code == 200
        data = response.json()
        assert str(data["id"]) == timer_id
        assert data["duration"] == 60


@pytest.mark.asyncio
async def test_get_timer_not_found():
    """Get non-existent timer returns 404."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/v1/timers/{fake_id}")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_start_timer():
    """Start a timer transitions to running."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_resp = await client.post("/api/v1/timers", json={"duration": 60})
        timer_id = create_resp.json()["id"]
        
        response = await client.post(f"/api/v1/timers/{timer_id}/start")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == TimerStatus.RUNNING.value


@pytest.mark.asyncio
async def test_stop_timer():
    """Stop a running timer transitions to paused."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_resp = await client.post("/api/v1/timers", json={"duration": 60})
        timer_id = create_resp.json()["id"]
        
        await client.post(f"/api/v1/timers/{timer_id}/start")
        response = await client.post(f"/api/v1/timers/{timer_id}/stop")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == TimerStatus.PAUSED.value


@pytest.mark.asyncio
async def test_reset_timer():
    """Reset a timer clears elapsed_time."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_resp = await client.post("/api/v1/timers", json={"duration": 60})
        timer_id = create_resp.json()["id"]
        
        await client.post(f"/api/v1/timers/{timer_id}/start")
        response = await client.post(f"/api/v1/timers/{timer_id}/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["elapsed_time"] == 0
        assert data["status"] == TimerStatus.IDLE.value


@pytest.mark.asyncio
async def test_update_timer_duration():
    """Update timer duration."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_resp = await client.post("/api/v1/timers", json={"duration": 60})
        timer_id = create_resp.json()["id"]
        
        response = await client.post(f"/api/v1/timers/{timer_id}", json={"duration": 120})
        assert response.status_code == 200
        data = response.json()
        assert data["duration"] == 120


@pytest.mark.asyncio
async def test_urgency_level_progression():
    """Urgency level increases with elapsed time."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_resp = await client.post("/api/v1/timers", json={"duration": 100})
        timer_id = create_resp.json()["id"]
        
        get_resp = await client.get(f"/api/v1/timers/{timer_id}")
        initial_urgency = get_resp.json()["urgency_level"]
        assert initial_urgency == 0
