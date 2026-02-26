import pytest
from httpx import AsyncClient
from uuid import UUID

from app.main import create_app


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """GET /health returns HTTP 200 with {"status": "ok"}."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_timer_returns_201(async_client: AsyncClient):
    """POST /api/v1/timers with {"duration": 60} returns HTTP 201 and valid UUID id."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    try:
        UUID(data["id"])
    except (ValueError, TypeError):
        pytest.fail(f"Invalid UUID: {data['id']}")
    assert data["duration"] == 60
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_create_timer_rejects_zero_duration(async_client: AsyncClient):
    """POST /api/v1/timers with duration <= 0 returns HTTP 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 0}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_timer_rejects_negative_duration(async_client: AsyncClient):
    """POST /api/v1/timers with negative duration returns HTTP 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": -10}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_start_timer_sets_running(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/start transitions timer to status=running."""
    create_response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_response.json()["id"]
    
    response = await async_client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer_sets_paused(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/stop transitions timer to status=paused."""
    create_response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_response.json()["id"]
    
    await async_client.post(f"/api/v1/timers/{timer_id}/start")
    
    response = await async_client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer_clears_elapsed(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/reset sets elapsed_time=0 and status=idle."""
    create_response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_response.json()["id"]
    
    await async_client.post(f"/api/v1/timers/{timer_id}/start")
    
    response = await async_client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_list_timers(async_client: AsyncClient):
    """GET /api/v1/timers returns list of all timers."""
    await async_client.post("/api/v1/timers", json={"duration": 60})
    await async_client.post("/api/v1/timers", json={"duration": 120})
    
    response = await async_client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "count" in data
    assert len(data["items"]) >= 2


@pytest.mark.asyncio
async def test_start_timer_nonexistent_returns_404(async_client: AsyncClient):
    """POST /api/v1/timers/{invalid_id}/start returns HTTP 404."""
    invalid_id = "00000000-0000-0000-0000-000000000000"
    response = await async_client.post(f"/api/v1/timers/{invalid_id}/start")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_stop_timer_nonexistent_returns_404(async_client: AsyncClient):
    """POST /api/v1/timers/{invalid_id}/stop returns HTTP 404."""
    invalid_id = "00000000-0000-0000-0000-000000000000"
    response = await async_client.post(f"/api/v1/timers/{invalid_id}/stop")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_reset_timer_nonexistent_returns_404(async_client: AsyncClient):
    """POST /api/v1/timers/{invalid_id}/reset returns HTTP 404."""
    invalid_id = "00000000-0000-0000-0000-000000000000"
    response = await async_client.post(f"/api/v1/timers/{invalid_id}/reset")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_timer_missing_duration_returns_400(async_client: AsyncClient):
    """POST /api/v1/timers without duration returns HTTP 400."""
    response = await async_client.post("/api/v1/timers", json={})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_timer_urgency_level_zero_when_idle(async_client: AsyncClient):
    """Newly created timer has urgency_level=0."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 100}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["urgency_level"] == 0
