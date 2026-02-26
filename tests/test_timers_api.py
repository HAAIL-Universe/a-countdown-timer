import pytest
from httpx import AsyncClient
from app.main import app
from app.database import get_pool


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient) -> None:
    """GET /health returns HTTP 200 with {"status": "ok"}."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_timer_returns_201(async_client: AsyncClient) -> None:
    """POST /api/v1/timers with {"duration": 60} returns HTTP 201 and a valid UUID id."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], str)
    assert len(data["id"]) == 36


@pytest.mark.asyncio
async def test_create_timer_rejects_zero_duration(async_client: AsyncClient) -> None:
    """POST /api/v1/timers with duration <= 0 returns HTTP 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 0}
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_create_timer_rejects_negative_duration(async_client: AsyncClient) -> None:
    """POST /api/v1/timers with negative duration returns HTTP 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": -10}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_start_timer_sets_running(async_client: AsyncClient) -> None:
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
async def test_stop_timer_sets_paused(async_client: AsyncClient) -> None:
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
async def test_reset_timer_clears_elapsed(async_client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/reset sets elapsed_time=0 and status=idle."""
    create_response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_response.json()["id"]

    response = await async_client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_list_timers_returns_200(async_client: AsyncClient) -> None:
    """GET /api/v1/timers returns HTTP 200 with items and count."""
    await async_client.post("/api/v1/timers", json={"duration": 60})
    await async_client.post("/api/v1/timers", json={"duration": 120})

    response = await async_client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "count" in data
    assert isinstance(data["items"], list)
    assert isinstance(data["count"], int)
    assert data["count"] >= 2


@pytest.mark.asyncio
async def test_list_timers_empty(async_client: AsyncClient) -> None:
    """GET /api/v1/timers returns empty list when no timers exist."""
    response = await async_client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["items"] == []


@pytest.mark.asyncio
async def test_start_nonexistent_timer_returns_404(async_client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/start with invalid id returns HTTP 404."""
    response = await async_client.post(
        "/api/v1/timers/00000000-0000-0000-0000-000000000000/start"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_stop_nonexistent_timer_returns_404(async_client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/stop with invalid id returns HTTP 404."""
    response = await async_client.post(
        "/api/v1/timers/00000000-0000-0000-0000-000000000000/stop"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_reset_nonexistent_timer_returns_404(async_client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/reset with invalid id returns HTTP 404."""
    response = await async_client.post(
        "/api/v1/timers/00000000-0000-0000-0000-000000000000/reset"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_timer_initializes_idle_state(async_client: AsyncClient) -> None:
    """Created timer has status=idle and elapsed_time=0."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 45}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "idle"
    assert data["elapsed_time"] == 0
    assert data["duration"] == 45


@pytest.mark.asyncio
async def test_timer_response_includes_urgency_level(async_client: AsyncClient) -> None:
    """Timer response includes urgency_level field."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    assert response.status_code == 201
    data = response.json()
    assert "urgency_level" in data
    assert isinstance(data["urgency_level"], int)


@pytest.mark.asyncio
async def test_invalid_request_body_returns_400(async_client: AsyncClient) -> None:
    """POST /api/v1/timers with invalid body returns HTTP 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"invalid_field": "value"}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_missing_duration_field_returns_400(async_client: AsyncClient) -> None:
    """POST /api/v1/timers without duration field returns HTTP 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={}
    )
    assert response.status_code == 400
