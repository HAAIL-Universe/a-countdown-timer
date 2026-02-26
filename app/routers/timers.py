from fastapi import APIRouter, HTTPException, status
from app.models.timer import Timer, TimerCreateRequest, TimerUpdateRequest
from app.services.timer_service import TimerService
from app.database import get_pool

router = APIRouter(prefix="/api/v1/timers", tags=["timers"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_timer(request: TimerCreateRequest) -> Timer:
    """Create a new timer."""
    if request.duration <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duration must be a positive integer in seconds"
        )
    pool = await get_pool()
    service = TimerService(pool)
    timer = await service.create_timer(request.duration)
    return timer


@router.get("")
async def list_timers() -> list[Timer]:
    """List all timers."""
    pool = await get_pool()
    service = TimerService(pool)
    timers = await service.list_timers()
    return timers


@router.post("/{timer_id}/start")
async def start_timer(timer_id: str) -> Timer:
    """Start countdown for a timer."""
    pool = await get_pool()
    service = TimerService(pool)
    try:
        timer = await service.start_timer(timer_id)
        return timer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{timer_id}/stop")
async def stop_timer(timer_id: str) -> Timer:
    """Pause countdown for a timer."""
    pool = await get_pool()
    service = TimerService(pool)
    try:
        timer = await service.stop_timer(timer_id)
        return timer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{timer_id}/reset")
async def reset_timer(timer_id: str) -> Timer:
    """Reset timer to elapsed_time=0 and status=idle."""
    pool = await get_pool()
    service = TimerService(pool)
    try:
        timer = await service.reset_timer(timer_id)
        return timer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{timer_id}")
async def update_timer(timer_id: str, request: TimerUpdateRequest) -> Timer:
    """Set or update timer duration."""
    if request.duration <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duration must be a positive integer in seconds"
        )
    pool = await get_pool()
    service = TimerService(pool)
    try:
        timer = await service.update_timer(timer_id, request.duration)
        return timer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
