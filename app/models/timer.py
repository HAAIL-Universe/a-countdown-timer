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
    """Timer entity model."""
    id: UUID
    duration: int = Field(..., description="Duration in seconds")
    elapsed_time: int = Field(default=0, description="Elapsed time in seconds")
    status: TimerStatus = Field(default=TimerStatus.idle)
    urgency_level: int = Field(default=0, description="0-3 based on elapsed percentage")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateTimerRequest(BaseModel):
    """Request to create a new timer."""
    duration: int = Field(..., gt=0, description="Duration in seconds, must be positive")


class TimerResponse(BaseModel):
    """Response model for timer data."""
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
