from fastapi import APIRouter, HTTPException, status
from uuid import UUID

from app.models.timer import (
    Timer,
    CreateTimerRequest,
    TimerResponse,
    TimerListResponse,
)
from app.services.timer_service import TimerService

router = APIRouter(prefix="/api/v1/timers", tags=["timers"])


@router.post("/", response_model=TimerResponse, status_code=status.HTTP_201_CREATED)
async def create_timer(payload: CreateTimerRequest) -> TimerResponse:
    """Create a new countdown timer."""
    service = TimerService()
    timer = await service.create(payload)
    return TimerResponse(**timer.dict())


@router.get("/", response_model=TimerListResponse)
async def list_timers() -> TimerListResponse:
    """List all timers."""
    service = TimerService()
    timers = await service.list_all()
    return TimerListResponse(
        items=[TimerResponse(**timer.dict()) for timer in timers],
        count=len(timers),
    )


@router.post("/{timer_id}/start", response_model=TimerResponse)
async def start_timer(timer_id: UUID) -> TimerResponse:
    """Start the countdown timer."""
    service = TimerService()
    timer = await service.start(timer_id)
    if timer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timer {timer_id} not found",
        )
    return TimerResponse(**timer.dict())


@router.post("/{timer_id}/stop", response_model=TimerResponse)
async def stop_timer(timer_id: UUID) -> TimerResponse:
    """Pause the countdown timer."""
    service = TimerService()
    timer = await service.stop(timer_id)
    if timer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timer {timer_id} not found",
        )
    return TimerResponse(**timer.dict())


@router.post("/{timer_id}/reset", response_model=TimerResponse)
async def reset_timer(timer_id: UUID) -> TimerResponse:
    """Reset the timer to zero elapsed time."""
    service = TimerService()
    timer = await service.reset(timer_id)
    if timer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timer {timer_id} not found",
        )
    return TimerResponse(**timer.dict())
