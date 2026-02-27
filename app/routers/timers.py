import uuid
from fastapi import APIRouter, HTTPException, Depends
from app.models.timer import Timer
from app.services.timer_service import TimerService
from app.database import get_pool

router = APIRouter(prefix="/api/v1/timers", tags=["timers"])


async def get_timer_service(pool=Depends(get_pool)) -> TimerService:
    """Provide TimerService with database pool."""
    return TimerService(pool)


@router.post("", status_code=201, response_model=Timer)
async def create_timer(
    duration: int,
    service: TimerService = Depends(get_timer_service),
) -> Timer:
    """Create a new timer with the given duration in seconds."""
    if duration <= 0:
        raise HTTPException(status_code=400, detail="Duration must be positive")
    return await service.create(duration)


@router.get("", response_model=list[Timer])
async def list_timers(service: TimerService = Depends(get_timer_service)) -> list[Timer]:
    """List all timers."""
    return await service.list_all()


@router.post("/{timer_id}/start", response_model=Timer)
async def start_timer(
    timer_id: str,
    service: TimerService = Depends(get_timer_service),
) -> Timer:
    """Start the countdown for a timer."""
    try:
        uuid.UUID(timer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timer ID")
    
    timer = await service.get(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    
    return await service.start(timer_id)


@router.post("/{timer_id}/stop", response_model=Timer)
async def stop_timer(
    timer_id: str,
    service: TimerService = Depends(get_timer_service),
) -> Timer:
    """Pause the countdown for a timer."""
    try:
        uuid.UUID(timer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timer ID")
    
    timer = await service.get(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    
    return await service.stop(timer_id)


@router.post("/{timer_id}/reset", response_model=Timer)
async def reset_timer(
    timer_id: str,
    service: TimerService = Depends(get_timer_service),
) -> Timer:
    """Reset a timer to elapsed_time=0 and status=idle."""
    try:
        uuid.UUID(timer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timer ID")
    
    timer = await service.get(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    
    return await service.reset(timer_id)
