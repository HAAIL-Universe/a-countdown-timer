from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer lifecycle states."""
    idle = "idle"
    running = "running"
    paused = "paused"
    complete = "complete"


class Timer(BaseModel):
    """Timer entity model (database representation)."""
    id: UUID
    duration: int
    elapsed_time: int
    status: TimerStatus
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateTimerRequest(BaseModel):
    """Request body for creating a new timer."""
    duration: int = Field(..., gt=0, description="Duration in seconds, must be positive")


class TimerResponse(BaseModel):
    """Response model for a single timer."""
    id: UUID
    duration: int
    elapsed_time: int
    status: TimerStatus
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TimerListResponse(BaseModel):
    """Response model for listing timers."""
    items: list[TimerResponse]
    count: int
