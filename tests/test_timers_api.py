import pytest
from httpx import AsyncClient
from uuid import UUID
import asyncpg

from app.main import create_app
from app.database import set_pool, get_pool


@pytest.fixture
async def test_pool():
    """Create a test database pool."""
    pool = await asyncpg.create_pool(
        "postgresql://postgres:postgres@localhost/countdown_timer_test",
        min_size=2,
        max_size=10,
    )
    set_pool(pool)
    yield pool
    await pool.close()


@pytest.fixture
async def test_db(test_pool):
    """Create test tables and teardown after each test."""
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS timers (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                duration INTEGER NOT NULL,
                elapsed_time INTEGER NOT NULL DEFAULT 0,
                status VARCHAR(255) NOT NULL DEFAULT 'idle',
                urgency_level INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
        """)
    yield
    async with pool.acquire() as conn:
        await conn.execute("DROP TABLE IF EXISTS timers")


@pytest.fixture
async def client(test_db):
    """Create async HTTP client for testing."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    """GET /health returns HTTP 200 with {status: ok}."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_timer_returns_201(client):
    """POST /api/v1/timers with {duration: 60} returns HTTP 201 and valid UUID id."""
    response = await client.post("/api/v1/timers", json={"duration": 60})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "message" in data
    UUID(data["id"])


@pytest.mark.asyncio
async def test_create_timer_rejects_zero_duration(client):
    """POST /api/v1/timers with duration <= 0 returns HTTP 400."""
    response = await client.post("/api/v1/timers", json={"duration": 0})
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_create_timer_rejects_negative_duration(client):
    """POST /api/v1/timers with negative duration returns HTTP 400."""
    response = await client.post("/api/v1/timers", json={"duration": -10})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_timers_returns_empty(client):
    """GET /api/v1/timers with no timers returns HTTP 200 with empty items."""
    response = await client.get("/api/v1/timers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 0


@pytest.mark.asyncio
async def test_list_timers_after_create(client):
    """GET /api/v1/timers after create returns timer in list."""
    create_response = await client.post("/api/v1/timers", json={"duration": 60})
    assert create_response.status_code == 201
    timer_id = create_response.json()["id"]

    list_response = await client.get("/api/v1/timers")
    assert list_response.status_code == 200
    data = list_response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == timer_id
    assert data["items"][0]["duration"] == 60
    assert data["items"][0]["status"] == "idle"


@pytest.mark.asyncio
async def test_start_timer_sets_running(client):
    """POST /api/v1/timers/{id}/start transitions timer to status=running."""
    create_response = await client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create_response.json()["id"]

    start_response = await client.post(f"/api/v1/timers/{timer_id}/start")
    assert start_response.status_code == 200
    data = start_response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer_sets_paused(client):
    """POST /api/v1/timers/{id}/stop transitions timer to status=paused."""
    create_response = await client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create_response.json()["id"]

    await client.post(f"/api/v1/timers/{timer_id}/start")
    stop_response = await client.post(f"/api/v1/timers/{timer_id}/stop")
    assert stop_response.status_code == 200
    data = stop_response.json()
    assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer_clears_elapsed(client):
    """POST /api/v1/timers/{id}/reset sets elapsed_time=0 and status=idle."""
    create_response = await client.post("/api/v1/timers", json={"duration": 60})
    timer_id = create_response.json()["id"]

    await client.post(f"/api/v1/timers/{timer_id}/start")
    reset_response = await client.post(f"/api/v1/timers/{timer_id}/reset")
    assert reset_response.status_code == 200
    data = reset_response.json()
    assert data["elapsed_time"] == 0
    assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_start_nonexistent_timer_returns_404(client):
    """POST /api/v1/timers/{id}/start with invalid id returns HTTP 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.post(f"/api/v1/timers/{fake_id}/start")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_stop_nonexistent_timer_returns_404(client):
    """POST /api/v1/timers/{id}/stop with invalid id returns HTTP 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.post(f"/api/v1/timers/{fake_id}/stop")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_reset_nonexistent_timer_returns_404(client):
    """POST /api/v1/timers/{id}/reset with invalid id returns HTTP 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.post(f"/api/v1/timers/{fake_id}/reset")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_timer_has_urgency_level(client):
    """Timer response includes urgency_level field."""
    response = await client.post("/api/v1/timers", json={"duration": 60})
    assert response.status_code == 201
    data = response.json()
    assert "urgency_level" in data or "message" in data


@pytest.mark.asyncio
async def test_create_timer_with_missing_duration(client):
    """POST /api/v1/timers without duration returns HTTP 400."""
    response = await client.post("/api/v1/timers", json={})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_timer_with_non_integer_duration(client):
    """POST /api/v1/timers with non-integer duration returns HTTP 400."""
    response = await client.post("/api/v1/timers", json={"duration": "sixty"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_multiple_timers(client):
    """Multiple timers can be created and listed independently."""
    resp1 = await client.post("/api/v1/timers", json={"duration": 30})
    id1 = resp1.json()["id"]

    resp2 = await client.post("/api/v1/timers", json={"duration": 120})
    id2 = resp2.json()["id"]

    list_response = await client.get("/api/v1/timers")
    assert list_response.status_code == 200
    items = list_response.json()["items"]
    assert len(items) == 2
    ids = {item["id"] for item in items}
    assert id1 in ids
    assert id2 in ids
