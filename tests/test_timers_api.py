"""Integration tests for all timer API endpoints."""
import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """GET /health returns HTTP 200 with status ok."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_timer_returns_201(async_client: AsyncClient):
    """POST /api/v1/timers with valid duration returns HTTP 201."""
    response = await async_client.post(
        "/api/v1/timers", json={"duration": 60}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["duration"] == 60
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"
    assert data["urgency_level"] == 0


@pytest.mark.asyncio
async def test_list_timers_returns_200(async_client: AsyncClient):
    """GET /api/v1/timers returns items and count."""
    # Create a timer first
    await async_client.post("/api/v1/timers", json={"duration": 30})

    response = await async_client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "count" in data
    assert data["count"] >= 1


@pytest.mark.asyncio
async def test_start_timer_sets_running(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/start transitions to running."""
    create = await async_client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create.json()["id"]

    response = await async_client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer_sets_paused(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/stop transitions to paused."""
    create = await async_client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create.json()["id"]
    await async_client.post(f"/api/v1/timers/{timer_id}/start")

    response = await async_client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    assert response.json()["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer_clears_elapsed(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/reset sets elapsed_time=0 and status=idle."""
    create = await async_client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create.json()["id"]
    await async_client.post(f"/api/v1/timers/{timer_id}/start")

    response = await async_client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_create_timer_rejects_zero_duration(async_client: AsyncClient):
    """POST /api/v1/timers with duration <= 0 returns HTTP 422."""
    response = await async_client.post(
        "/api/v1/timers", json={"duration": 0}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_start_nonexistent_timer_returns_404(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/start with bad ID returns 404."""
    response = await async_client.post(
        "/api/v1/timers/00000000-0000-0000-0000-000000000000/start"
    )
    assert response.status_code == 404
