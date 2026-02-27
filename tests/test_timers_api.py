import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from app.main import create_app


@pytest.fixture
def app():
    """Create a test FastAPI application."""
    return create_app()


@pytest.mark.asyncio
async def test_health_check(app):
    """Test health check endpoint returns ok status."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_timer(app):
    """Test creating a new countdown timer."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "duration": 60,
            "elapsed_time": 0,
            "status": "idle",
            "urgency_level": 0
        }
        with patch("app.repos.timer.TimerRepository.create") as mock_create:
            timer_id = str(uuid4())
            mock_create.return_value = {
                "id": timer_id,
                "duration": 60,
                "elapsed_time": 0,
                "status": "idle",
                "urgency_level": 0,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
            response = await client.post("/api/v1/timers", json=payload)
            assert response.status_code == 201
            data = response.json()
            assert "id" in data
            assert data["duration"] == 60


@pytest.mark.asyncio
async def test_list_timers(app):
    """Test listing all timers."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        with patch("app.repos.timer.TimerRepository.list_all") as mock_list:
            mock_list.return_value = [
                {
                    "id": str(uuid4()),
                    "duration": 60,
                    "elapsed_time": 10,
                    "status": "running",
                    "urgency_level": 1,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:10Z"
                }
            ]
            response = await client.get("/api/v1/timers")
            assert response.status_code == 200
            data = response.json()
            assert "items" in data
            assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_start_timer(app):
    """Test starting a countdown timer."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        timer_id = str(uuid4())
        with patch("app.repos.timer.TimerRepository.get_by_id") as mock_get, \
             patch("app.repos.timer.TimerRepository.update") as mock_update:
            mock_get.return_value = {
                "id": timer_id,
                "duration": 60,
                "elapsed_time": 0,
                "status": "idle",
                "urgency_level": 0,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
            mock_update.return_value = {
                "id": timer_id,
                "duration": 60,
                "elapsed_time": 0,
                "status": "running",
                "urgency_level": 0,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
            response = await client.post(f"/api/v1/timers/{timer_id}/start")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_timer(app):
    """Test pausing a countdown timer."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        timer_id = str(uuid4())
        with patch("app.repos.timer.TimerRepository.get_by_id") as mock_get, \
             patch("app.repos.timer.TimerRepository.update") as mock_update:
            mock_get.return_value = {
                "id": timer_id,
                "duration": 60,
                "elapsed_time": 10,
                "status": "running",
                "urgency_level": 0,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:10Z"
            }
            mock_update.return_value = {
                "id": timer_id,
                "duration": 60,
                "elapsed_time": 10,
                "status": "paused",
                "urgency_level": 0,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:10Z"
            }
            response = await client.post(f"/api/v1/timers/{timer_id}/stop")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "paused"


@pytest.mark.asyncio
async def test_reset_timer(app):
    """Test resetting a timer to zero elapsed time."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        timer_id = str(uuid4())
        with patch("app.repos.timer.TimerRepository.get_by_id") as mock_get, \
             patch("app.repos.timer.TimerRepository.update") as mock_update:
            mock_get.return_value = {
                "id": timer_id,
                "duration": 60,
                "elapsed_time": 10,
                "status": "paused",
                "urgency_level": 0,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:10Z"
            }
            mock_update.return_value = {
                "id": timer_id,
                "duration": 60,
                "elapsed_time": 0,
                "status": "idle",
                "urgency_level": 0,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:10Z"
            }
            response = await client.post(f"/api/v1/timers/{timer_id}/reset")
            assert response.status_code == 200
            data = response.json()
            assert data["elapsed_time"] == 0
            assert data["status"] == "idle"


@pytest.mark.asyncio
async def test_create_timer_validation_error(app):
    """Test creating a timer with invalid duration."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "duration": -10,
            "elapsed_time": 0,
            "status": "idle",
            "urgency_level": 0
        }
        response = await client.post("/api/v1/timers", json=payload)
        assert response.status_code == 400
        data = response.json()
        assert "error" in data or "detail" in data


@pytest.mark.asyncio
async def test_timer_not_found(app):
    """Test accessing a non-existent timer."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        timer_id = str(uuid4())
        with patch("app.repos.timer.TimerRepository.get_by_id") as mock_get:
            mock_get.return_value = None
            response = await client.get(f"/api/v1/timers/{timer_id}")
            assert response.status_code == 404
