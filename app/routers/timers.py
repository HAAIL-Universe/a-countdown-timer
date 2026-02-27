from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_pool
from app.repos.timer_repo import TimerRepo
from app.services.timer_service import TimerService
from app.models.timer import (
    CreateTimerRequest,
    TimerResponse,
    TimerListResponse,
)

router = APIRouter(prefix="/api/v1/timers", tags=["timers"])


async def get_timer_service() -> TimerService:
    """Dependency: build TimerService from pool -> repo -> service."""
    pool = await get_pool()
    repo = TimerRepo(pool)
    return TimerService(repo)


@router.post("", status_code=201, response_model=TimerResponse)
async def create_timer(
    body: CreateTimerRequest,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Create a new timer with the given duration in seconds."""
    timer = await service.create_timer(body.duration)
    return TimerResponse.model_validate(timer, from_attributes=True)


@router.get("", response_model=TimerListResponse)
async def list_timers(
    service: TimerService = Depends(get_timer_service),
) -> TimerListResponse:
    """List all timers with current status and urgency_level."""
    timers = await service.list_timers()
    items = [TimerResponse.model_validate(t, from_attributes=True) for t in timers]
    return TimerListResponse(items=items, count=len(items))


@router.get("/{timer_id}", response_model=TimerResponse)
async def get_timer(
    timer_id: UUID,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Retrieve details of a specific timer."""
    timer = await service._repo.get_by_id(timer_id)
    if timer is None:
        raise HTTPException(status_code=404, detail="Timer not found")
    return TimerResponse.model_validate(timer, from_attributes=True)


@router.post("/{timer_id}/start", response_model=TimerResponse)
async def start_timer(
    timer_id: UUID,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Start a timer by setting status to running."""
    timer = await service.start_timer(timer_id)
    if timer is None:
        raise HTTPException(status_code=404, detail="Timer not found")
    return TimerResponse.model_validate(timer, from_attributes=True)


@router.post("/{timer_id}/stop", response_model=TimerResponse)
async def stop_timer(
    timer_id: UUID,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Stop a timer by setting status to paused."""
    timer = await service.stop_timer(timer_id)
    if timer is None:
        raise HTTPException(status_code=404, detail="Timer not found")
    return TimerResponse.model_validate(timer, from_attributes=True)


@router.post("/{timer_id}/reset", response_model=TimerResponse)
async def reset_timer(
    timer_id: UUID,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Reset a timer to idle status with elapsed_time=0."""
    timer = await service.reset_timer(timer_id)
    if timer is None:
        raise HTTPException(status_code=404, detail="Timer not found")
    return TimerResponse.model_validate(timer, from_attributes=True)


@router.post("/{timer_id}/tick", response_model=TimerResponse)
async def tick_timer(
    timer_id: UUID,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Advance the timer by 1 second. Called by the client each second while running."""
    timer = await service.tick_timer(timer_id)
    if timer is None:
        raise HTTPException(status_code=404, detail="Timer not found")
    return TimerResponse.model_validate(timer, from_attributes=True)
