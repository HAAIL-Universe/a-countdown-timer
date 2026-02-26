import pytest
from httpx import AsyncClient
from uuid import UUID


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """GET /health returns 200 with status ok."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_create_timer_returns_201(async_client: AsyncClient):
    """POST /api/v1/timers with duration returns 201 and timer with valid UUID."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["duration"] == 60
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"
    UUID(data["id"])


@pytest.mark.asyncio
async def test_list_timers_returns_200(async_client: AsyncClient):
    """GET /api/v1/timers returns 200 with timer list."""
    await async_client.post("/api/v1/timers", json={"duration": 60})
    await async_client.post("/api/v1/timers", json={"duration": 120})
    
    response = await async_client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_start_timer_sets_running(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/start transitions timer to running."""
    create_resp = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60},
    )
    timer_id = create_resp.json()["id"]
    
    response = await async_client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer_sets_paused(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/stop transitions timer to paused."""
    create_resp = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60},
    )
    timer_id = create_resp.json()["id"]
    
    await async_client.post(f"/api/v1/timers/{timer_id}/start")
    response = await async_client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer_clears_elapsed(async_client: AsyncClient):
    """POST /api/v1/timers/{id}/reset sets elapsed_time=0 and status=idle."""
    create_resp = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60},
    )
    timer_id = create_resp.json()["id"]
    
    response = await async_client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_create_timer_rejects_zero_duration(async_client: AsyncClient):
    """POST /api/v1/timers with duration <= 0 returns 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 0},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_timer_rejects_negative_duration(async_client: AsyncClient):
    """POST /api/v1/timers with negative duration returns 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": -10},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_timer_rejects_missing_duration(async_client: AsyncClient):
    """POST /api/v1/timers without duration returns 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={},
    )
    assert response.status_code == 400
