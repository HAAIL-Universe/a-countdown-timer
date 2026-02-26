from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.models.timer import Timer, TimerCreateRequest, TimerResponse
from app.services.timer_service import TimerService

router = APIRouter(prefix="/api/v1/timers", tags=["timers"])


@router.post("", response_model=TimerResponse, status_code=status.HTTP_201_CREATED)
async def create_timer(payload: TimerCreateRequest, service: TimerService) -> TimerResponse:
    """Create a new countdown timer."""
    if payload.duration <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duration must be greater than 0",
        )
    timer = await service.create_timer(payload.duration)
    return TimerResponse.model_validate(timer)


@router.get("", response_model=list[TimerResponse])
async def list_timers(service: TimerService) -> list[TimerResponse]:
    """List all timers."""
    timers = await service.list_timers()
    return [TimerResponse.model_validate(t) for t in timers]


@router.post("/{timer_id}/start", response_model=TimerResponse)
async def start_timer(timer_id: UUID, service: TimerService) -> TimerResponse:
    """Start a timer."""
    timer = await service.start_timer(timer_id)
    if timer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found",
        )
    return TimerResponse.model_validate(timer)


@router.post("/{timer_id}/stop", response_model=TimerResponse)
async def stop_timer(timer_id: UUID, service: TimerService) -> TimerResponse:
    """Stop a timer."""
    timer = await service.stop_timer(timer_id)
    if timer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found",
        )
    return TimerResponse.model_validate(timer)


@router.post("/{timer_id}/reset", response_model=TimerResponse)
async def reset_timer(timer_id: UUID, service: TimerService) -> TimerResponse:
    """Reset a timer to zero elapsed time."""
    timer = await service.reset_timer(timer_id)
    if timer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found",
        )
    return TimerResponse.model_validate(timer)
