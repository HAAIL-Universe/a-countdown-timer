from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.models.timer import TimerCreate, TimerResponse, TimerStatus
from app.services.timer_service import TimerService
from app.repos.timer_repo import TimerRepo
from app.database import get_pool

router = APIRouter(prefix="/api/v1/timers", tags=["timers"])


async def get_timer_service() -> TimerService:
    """Dependency: inject TimerService with repo."""
    pool = await get_pool()
    repo = TimerRepo(pool)
    return TimerService(repo)


@router.post("/", response_model=TimerResponse, status_code=status.HTTP_201_CREATED)
async def create_timer(
    payload: TimerCreate,
    service: TimerService = None,
) -> TimerResponse:
    """Create a new countdown timer."""
    if service is None:
        service = await get_timer_service()
    try:
        timer = await service.create_timer(payload.duration)
        return TimerResponse(**timer.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[TimerResponse])
async def list_timers(
    service: TimerService = None,
) -> list[TimerResponse]:
    """List all timers."""
    if service is None:
        service = await get_timer_service()
    timers = await service.list_timers()
    return [TimerResponse(**timer.model_dump()) for timer in timers]


@router.post("/{timer_id}/start", response_model=TimerResponse)
async def start_timer(
    timer_id: UUID,
    service: TimerService = None,
) -> TimerResponse:
    """Start the countdown timer from current elapsed time."""
    if service is None:
        service = await get_timer_service()
    try:
        timer = await service.start_timer(timer_id)
        return TimerResponse(**timer.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{timer_id}/stop", response_model=TimerResponse)
async def stop_timer(
    timer_id: UUID,
    service: TimerService = None,
) -> TimerResponse:
    """Pause the countdown timer at current elapsed time."""
    if service is None:
        service = await get_timer_service()
    try:
        timer = await service.stop_timer(timer_id)
        return TimerResponse(**timer.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{timer_id}/reset", response_model=TimerResponse)
async def reset_timer(
    timer_id: UUID,
    service: TimerService = None,
) -> TimerResponse:
    """Reset the timer to zero elapsed time and idle status."""
    if service is None:
        service = await get_timer_service()
    try:
        timer = await service.reset_timer(timer_id)
        return TimerResponse(**timer.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
