from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer operational state."""
    idle = "idle"
    running = "running"
    paused = "paused"
    complete = "complete"


class Timer(BaseModel):
    """Core Timer domain model."""
    id: UUID
    duration: int = Field(..., gt=0, description="Duration in seconds")
    elapsed_time: int = Field(default=0, ge=0, description="Elapsed time in seconds")
    status: TimerStatus = Field(default=TimerStatus.idle)
    urgency_level: int = Field(default=0, ge=0, le=3, description="0=low, 1=medium, 2=high, 3=critical")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateTimerRequest(BaseModel):
    """Request to create a new timer."""
    duration: int = Field(..., gt=0, description="Duration in seconds")


class TimerResponse(BaseModel):
    """Response containing a single timer."""
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
    """Response containing a list of timers."""
    items: list[TimerResponse]
    count: int = Field(..., ge=0, description="Total count of timers")
