from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from app.services.timer_service import TimerService
from app.models.timer import Timer
from app.database import get_pool

router = APIRouter(prefix="/api/v1/timers", tags=["timers"])


class CreateTimerRequest(BaseModel):
    """Request to create a new timer."""
    duration: int = Field(..., gt=0, description="Duration in seconds, must be positive")


class UpdateDurationRequest(BaseModel):
    """Request to update timer duration."""
    duration: int = Field(..., gt=0, description="Duration in seconds, must be positive")


class TimerResponse(BaseModel):
    """Timer state response."""
    id: UUID
    duration: int
    elapsed_time: int
    status: str
    urgency_level: int

    class Config:
        from_attributes = True


async def get_timer_service(pool=Depends(get_pool)) -> TimerService:
    """Inject TimerService with database pool."""
    return TimerService(pool)


@router.post("", status_code=201, response_model=TimerResponse)
async def create_timer(
    req: CreateTimerRequest,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Create a new countdown timer."""
    timer = await service.create_timer(duration=req.duration)
    return TimerResponse.model_validate(timer)


@router.get("", response_model=list[TimerResponse])
async def list_timers(
    service: TimerService = Depends(get_timer_service),
) -> list[TimerResponse]:
    """List all timers with current status."""
    timers = await service.list_timers()
    return [TimerResponse.model_validate(t) for t in timers]


@router.post("/{timer_id}", response_model=TimerResponse)
async def update_timer_duration(
    timer_id: UUID,
    req: UpdateDurationRequest,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Set or update timer duration in seconds."""
    timer = await service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    updated = await service.set_duration(timer_id, req.duration)
    return TimerResponse.model_validate(updated)


@router.post("/{timer_id}/start", response_model=TimerResponse)
async def start_timer(
    timer_id: UUID,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Start countdown from current elapsed_time."""
    timer = await service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    updated = await service.start_timer(timer_id)
    return TimerResponse.model_validate(updated)


@router.post("/{timer_id}/stop", response_model=TimerResponse)
async def stop_timer(
    timer_id: UUID,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Pause countdown at current elapsed_time."""
    timer = await service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    updated = await service.stop_timer(timer_id)
    return TimerResponse.model_validate(updated)


@router.post("/{timer_id}/reset", response_model=TimerResponse)
async def reset_timer(
    timer_id: UUID,
    service: TimerService = Depends(get_timer_service),
) -> TimerResponse:
    """Reset elapsed_time to 0 and set status to idle."""
    timer = await service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    updated = await service.reset_timer(timer_id)
    return TimerResponse.model_validate(updated)
