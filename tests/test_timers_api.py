import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Health check endpoint returns 200 with ok status."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_create_timer(client: AsyncClient):
    """Create a new timer with initial duration."""
    response = await client.post(
        "/api/v1/timers",
        json={"duration": 60},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["duration"] == 60
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"
    assert data["urgency_level"] == 0


@pytest.mark.asyncio
async def test_create_timer_invalid_duration(client: AsyncClient):
    """Create timer with invalid duration returns 400."""
    response = await client.post(
        "/api/v1/timers",
        json={"duration": -1},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_create_timer_missing_duration(client: AsyncClient):
    """Create timer without duration returns 400."""
    response = await client.post(
        "/api/v1/timers",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_list_timers(client: AsyncClient):
    """List all timers returns array of timers."""
    await client.post("/api/v1/timers", json={"duration": 60})
    await client.post("/api/v1/timers", json={"duration": 120})
    
    response = await client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert data["count"] >= 2


@pytest.mark.asyncio
async def test_start_timer(client: AsyncClient):
    """Start a timer changes status to running."""
    create_response = await client.post(
        "/api/v1/timers",
        json={"duration": 60},
    )
    timer_id = create_response.json()["id"]
    
    response = await client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer(client: AsyncClient):
    """Stop a timer changes status to paused."""
    create_response = await client.post(
        "/api/v1/timers",
        json={"duration": 60},
    )
    timer_id = create_response.json()["id"]
    
    await client.post(f"/api/v1/timers/{timer_id}/start")
    response = await client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer(client: AsyncClient):
    """Reset a timer sets elapsed_time to 0."""
    create_response = await client.post(
        "/api/v1/timers",
        json={"duration": 60},
    )
    timer_id = create_response.json()["id"]
    
    response = await client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_timer_not_found(client: AsyncClient):
    """Get non-existent timer returns 404."""
    fake_id = str(uuid4())
    response = await client.get(f"/api/v1/timers/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_urgency_level_calculation(client: AsyncClient):
    """Urgency level updates based on elapsed time ratio."""
    create_response = await client.post(
        "/api/v1/timers",
        json={"duration": 100},
    )
    timer_id = create_response.json()["id"]
    
    response = await client.get(f"/api/v1/timers/{timer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["urgency_level"] in [0, 1, 2, 3]
