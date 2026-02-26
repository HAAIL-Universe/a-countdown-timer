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
    """Internal Timer domain model."""
    id: UUID
    duration: int = Field(..., description="Total duration in seconds")
    elapsed_time: int = Field(..., description="Time elapsed in seconds")
    status: TimerStatus
    urgency_level: int = Field(..., ge=0, le=3, description="0-3 urgency level")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateTimerRequest(BaseModel):
    """Request to create a new timer."""
    duration: int = Field(..., gt=0, description="Total duration in seconds")


class TimerResponse(BaseModel):
    """API response for a single timer."""
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
    """API response for list of timers."""
    items: list[TimerResponse]
    count: int = Field(..., ge=0, description="Total count of timers")
