import pytest
from httpx import AsyncClient
from uuid import UUID

from app.main import create_app
from app.database import get_pool, close_pool, init_db


@pytest.fixture
async def test_app():
    """Create test app with isolated database."""
    app = create_app()
    await init_db()
    yield app
    await close_pool()


@pytest.fixture
async def async_client(test_app):
    """Create async test client."""
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health_check(async_client):
    """GET /health returns HTTP 200 with {status: ok}."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_create_timer_returns_201(async_client):
    """POST /api/v1/timers with {duration: 60} returns HTTP 201 and valid UUID id."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    try:
        UUID(data["id"])
    except ValueError:
        pytest.fail(f"Invalid UUID: {data['id']}")
    assert data["duration"] == 60
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_start_timer_sets_running(async_client):
    """POST /api/v1/timers/{id}/start transitions timer to status=running."""
    create_resp = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_resp.json()["id"]

    response = await async_client.post(f"/api/v1/timers/{timer_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer_sets_paused(async_client):
    """POST /api/v1/timers/{id}/stop transitions timer to status=paused."""
    create_resp = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_resp.json()["id"]

    await async_client.post(f"/api/v1/timers/{timer_id}/start")

    response = await async_client.post(f"/api/v1/timers/{timer_id}/stop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer_clears_elapsed(async_client):
    """POST /api/v1/timers/{id}/reset sets elapsed_time=0 and status=idle."""
    create_resp = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_resp.json()["id"]

    await async_client.post(f"/api/v1/timers/{timer_id}/start")

    response = await async_client.post(f"/api/v1/timers/{timer_id}/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_create_timer_rejects_zero_duration(async_client):
    """POST /api/v1/timers with duration <= 0 returns HTTP 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 0}
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data or "detail" in data


@pytest.mark.asyncio
async def test_create_timer_rejects_negative_duration(async_client):
    """POST /api/v1/timers with duration < 0 returns HTTP 400."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": -10}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_timers_returns_200(async_client):
    """GET /api/v1/timers returns HTTP 200 with items and count."""
    await async_client.post("/api/v1/timers", json={"duration": 60})
    await async_client.post("/api/v1/timers", json={"duration": 120})

    response = await async_client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "count" in data
    assert data["count"] >= 2
    assert len(data["items"]) >= 2


@pytest.mark.asyncio
async def test_nonexistent_timer_returns_404(async_client):
    """GET /api/v1/timers/{id} for nonexistent timer returns HTTP 404."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = await async_client.get(f"/api/v1/timers/{fake_uuid}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_start_nonexistent_timer_returns_404(async_client):
    """POST /api/v1/timers/{id}/start for nonexistent timer returns HTTP 404."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = await async_client.post(f"/api/v1/timers/{fake_uuid}/start")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_stop_nonexistent_timer_returns_404(async_client):
    """POST /api/v1/timers/{id}/stop for nonexistent timer returns HTTP 404."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = await async_client.post(f"/api/v1/timers/{fake_uuid}/stop")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_reset_nonexistent_timer_returns_404(async_client):
    """POST /api/v1/timers/{id}/reset for nonexistent timer returns HTTP 404."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = await async_client.post(f"/api/v1/timers/{fake_uuid}/reset")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_timer_response_contains_all_fields(async_client):
    """Timer response includes id, duration, elapsed_time, status, urgency_level."""
    response = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    data = response.json()
    assert "id" in data
    assert "duration" in data
    assert "elapsed_time" in data
    assert "status" in data
    assert "urgency_level" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_timer_status_transitions(async_client):
    """Timer status transitions correctly: idle -> running -> paused -> idle."""
    create_resp = await async_client.post(
        "/api/v1/timers",
        json={"duration": 60}
    )
    timer_id = create_resp.json()["id"]
    assert create_resp.json()["status"] == "idle"

    start_resp = await async_client.post(f"/api/v1/timers/{timer_id}/start")
    assert start_resp.json()["status"] == "running"

    stop_resp = await async_client.post(f"/api/v1/timers/{timer_id}/stop")
    assert stop_resp.json()["status"] == "paused"

    reset_resp = await async_client.post(f"/api/v1/timers/{timer_id}/reset")
    assert reset_resp.json()["status"] == "idle"
