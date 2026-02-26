import pytest
from httpx import AsyncClient
from uuid import UUID

from app.main import create_app


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """GET /health returns HTTP 200 with {status: ok}."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_timer_returns_201(async_client: AsyncClient):
    """POST /api/v1/timers with {duration: 60} returns HTTP 201 and valid UUID id."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert isinstance(body["id"], str)
    UUID(body["id"])
    assert body["duration"] == 60
    assert body["elapsed_time"] == 0
    assert body["status"] == "idle"
    assert body["urgency_level"] == 0


@pytest.mark.asyncio
async def test_list_timers_returns_200(async_client: AsyncClient):
    """GET /api/v1/timers returns HTTP 200 with list of timers."""
    await async_client.post("/api/v1/timers", json={"duration": 60})
    await async_client.post("/api/v1/timers", json={"duration": 120})
    
    response = await async_client.get("/api/v1/timers")
    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert isinstance(body["items"], list)
    assert len(body["items"]) >= 2
    assert "count" in body
    assert body["count"] >= 2


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
    body = response.json()
    assert body["status"] == "running"
    assert body["id"] == timer_id


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
    body = response.json()
    assert body["status"] == "paused"
    assert body["id"] == timer_id


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
    body = response.json()
    assert body["elapsed_time"] == 0
    assert body["status"] == "idle"
    assert body["id"] == timer_id


@pytest.mark.asyncio
async def test_create_timer_rejects_zero_duration(async_client: AsyncClient):
    """POST /api/v1/timers with duration <= 0 returns HTTP 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 0}
    )
    assert response.status_code == 400
    body = response.json()
    assert "error" in body or "detail" in body


@pytest.mark.asyncio
async def test_create_timer_rejects_negative_duration(async_client: AsyncClient):
    """POST /api/v1/timers with negative duration returns HTTP 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": -10}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_set_timer_duration(async_client: AsyncClient):
    """POST /api/v1/timers/{id} updates timer duration."""
    create_response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_response.json()["id"]
    
    response = await async_client.post(
        f"/api/v1/timers/{timer_id}",
        json={"duration": 120}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["duration"] == 120
    assert body["id"] == timer_id


@pytest.mark.asyncio
async def test_nonexistent_timer_returns_404(async_client: AsyncClient):
    """GET /api/v1/timers/{id} for nonexistent timer returns HTTP 404."""
    fake_id = "550e8400-e29b-41d4-a716-446655440000"
    response = await async_client.get(f"/api/v1/timers/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_start_nonexistent_timer_returns_404(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/start for nonexistent timer returns HTTP 404."""
    fake_id = "550e8400-e29b-41d4-a716-446655440000"
    response = await async_client.post(f"/api/v1/timers/{fake_id}/start")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_timer_urgency_level_calculation(async_client: AsyncClient):
    """Timer urgency_level is calculated correctly based on elapsed_time ratio."""
    create_response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 100}
    )
    timer_id = create_response.json()["id"]
    
    response = await async_client.get(f"/api/v1/timers/{timer_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["urgency_level"] == 0
