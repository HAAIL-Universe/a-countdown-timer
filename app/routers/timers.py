from fastapi import APIRouter, HTTPException
from uuid import UUID

from app.models.timer import Timer, TimerCreateRequest, TimerUpdateDurationRequest
from app.services.timer_service import TimerService

router = APIRouter(prefix="/api/v1/timers", tags=["timers"])


@router.post("", status_code=201)
async def create_timer(req: TimerCreateRequest, service: TimerService) -> Timer:
    """Create a new timer with the given duration."""
    if req.duration <= 0:
        raise HTTPException(status_code=400, detail="Duration must be a positive integer")
    return await service.create_timer(req.duration)


@router.get("")
async def list_timers(service: TimerService) -> list[Timer]:
    """List all timers with their current status and urgency level."""
    return await service.list_timers()


@router.post("/{timer_id}/start", status_code=200)
async def start_timer(timer_id: UUID, service: TimerService) -> Timer:
    """Start countdown for the given timer."""
    timer = await service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    return await service.start_timer(timer_id)


@router.post("/{timer_id}/stop", status_code=200)
async def stop_timer(timer_id: UUID, service: TimerService) -> Timer:
    """Pause countdown at the current elapsed time."""
    timer = await service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    return await service.stop_timer(timer_id)


@router.post("/{timer_id}/reset", status_code=200)
async def reset_timer(timer_id: UUID, service: TimerService) -> Timer:
    """Reset elapsed time to 0 and set status to idle."""
    timer = await service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    return await service.reset_timer(timer_id)


@router.post("/{timer_id}", status_code=200)
async def update_timer_duration(
    timer_id: UUID, req: TimerUpdateDurationRequest, service: TimerService
) -> Timer:
    """Set or update timer duration in seconds."""
    if req.duration <= 0:
        raise HTTPException(status_code=400, detail="Duration must be a positive integer")
    timer = await service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    return await service.update_duration(timer_id, req.duration)
