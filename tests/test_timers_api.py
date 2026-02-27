import pytest
import uuid
from httpx import AsyncClient
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
    try:
        uuid.UUID(data["id"])
    except (ValueError, TypeError):
        pytest.fail("Returned id is not a valid UUID")
    assert data["duration"] == 60
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_list_timers_returns_200(client: AsyncClient) -> None:
    """GET /api/v1/timers returns HTTP 200 with a list of timers."""
    await client.post("/api/v1/timers", json={"duration": 60})
    response = await client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert "count" in data
    assert data["count"] >= 1


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
    
    response = await client.post("/api/v1/timers", json={"duration": -10})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_start_nonexistent_timer_returns_404(client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/start with nonexistent id returns HTTP 404."""
    fake_id = str(uuid.uuid4())
    response = await client.post(f"/api/v1/timers/{fake_id}/start")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_stop_nonexistent_timer_returns_404(client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/stop with nonexistent id returns HTTP 404."""
    fake_id = str(uuid.uuid4())
    response = await client.post(f"/api/v1/timers/{fake_id}/stop")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_reset_nonexistent_timer_returns_404(client: AsyncClient) -> None:
    """POST /api/v1/timers/{id}/reset with nonexistent id returns HTTP 404."""
    fake_id = str(uuid.uuid4())
    response = await client.post(f"/api/v1/timers/{fake_id}/reset")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_timer_missing_duration_returns_400(client: AsyncClient) -> None:
    """POST /api/v1/timers without duration field returns HTTP 400."""
    response = await client.post("/api/v1/timers", json={})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_timer_initial_urgency_level(client: AsyncClient) -> None:
    """New timer has urgency_level=0."""
    response = await client.post("/api/v1/timers", json={"duration": 60})
    assert response.status_code == 201
    data = response.json()
    assert data["urgency_level"] == 0
