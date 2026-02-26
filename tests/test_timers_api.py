import pytest
from httpx import AsyncClient
from uuid import UUID
from app.main import app
from app.database import get_pool


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """GET /health returns HTTP 200 with {"status": "ok"}."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_timer_returns_201(client: AsyncClient) -> None:
    """POST /api/v1/timers with {"duration": 60} returns HTTP 201 and a valid UUID id."""
    response = await client.post("/api/v1/timers", json={"duration": 60})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    UUID(data["id"])
    assert data["duration"] == 60
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_list_timers_returns_200(client: AsyncClient) -> None:
    """GET /api/v1/timers returns HTTP 200 with items array."""
    await client.post("/api/v1/timers", json={"duration": 60})
    response = await client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert "count" in data


@pytest.mark.asyncio
async def test_start_timer_sets_running(client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/start transitions timer to status=running."""
    create_response = await client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create_response.json()["id"]
    
    response = await client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer_sets_paused(client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/stop transitions timer to status=paused."""
    create_response = await client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create_response.json()["id"]
    
    await client.post(f"/api/v1/timers/{timer_id}/start")
    response = await client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer_clears_elapsed(client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/reset sets elapsed_time=0 and status=idle."""
    create_response = await client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create_response.json()["id"]
    
    await client.post(f"/api/v1/timers/{timer_id}/start")
    response = await client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_create_timer_rejects_zero_duration(client: AsyncClient) -> None:
    """POST /api/v1/timers with duration <= 0 returns HTTP 400."""
    response = await client.post("/api/v1/timers", json={"duration": 0})
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_create_timer_rejects_negative_duration(client: AsyncClient) -> None:
    """POST /api/v1/timers with negative duration returns HTTP 400."""
    response = await client.post("/api/v1/timers", json={"duration": -10})
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_update_timer_duration(client: AsyncClient) -> None:
    """POST /api/v1/timers/{id} updates timer duration."""
    create_response = await client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create_response.json()["id"]
    
    response = await client.post(f"/api/v1/timers/{timer_id}", json={"duration": 120})
    assert response.status_code == 200
    data = response.json()
    assert data["duration"] == 120


@pytest.mark.asyncio
async def test_get_single_timer(client: AsyncClient) -> None:
    """GET /api/v1/timers/{id} returns the timer."""
    create_response = await client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create_response.json()["id"]
    
    response = await client.get(f"/api/v1/timers/{timer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == timer_id
    assert data["duration"] == 60


@pytest.mark.asyncio
async def test_get_nonexistent_timer_returns_404(client: AsyncClient) -> None:
    """GET /api/v1/timers/{id} with invalid id returns HTTP 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/api/v1/timers/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_start_nonexistent_timer_returns_404(client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/start with invalid id returns HTTP 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.post(f"/api/v1/timers/{fake_id}/start")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_timer_urgency_level_progression(client: AsyncClient) -> None:
    """Timer urgency_level reflects elapsed_time to duration ratio."""
    create_response = await client.post("/api/v1/timers", json={"duration": 100})
    timer_id = create_response.json()["id"]
    
    response = await client.get(f"/api/v1/timers/{timer_id}")
    data = response.json()
    assert data["urgency_level"] == 0


@pytest.mark.asyncio
async def test_create_timer_missing_duration(client: AsyncClient) -> None:
    """POST /api/v1/timers without duration returns HTTP 400."""
    response = await client.post("/api/v1/timers", json={})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_timer_rejects_invalid_duration(client: AsyncClient) -> None:
    """POST /api/v1/timers/{id} with invalid duration returns HTTP 400."""
    create_response = await client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create_response.json()["id"]
    
    response = await client.post(f"/api/v1/timers/{timer_id}", json={"duration": 0})
    assert response.status_code == 400
