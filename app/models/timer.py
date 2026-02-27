from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer lifecycle states."""
    idle = "idle"
    running = "running"
    paused = "paused"
    complete = "complete"


class Timer(BaseModel):
    """Countdown timer entity."""
    id: UUID
    duration: int = Field(..., gt=0, description="Total duration in seconds")
    elapsed_time: int = Field(default=0, ge=0, description="Elapsed seconds")
    status: TimerStatus
    urgency_level: int = Field(default=0, ge=0, le=3, description="0-3 urgency scale")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateTimerRequest(BaseModel):
    """Request to create a new timer."""
    duration: int = Field(..., gt=0, description="Duration in seconds")


class TimerResponse(BaseModel):
    """Timer response model for API endpoints."""
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
    """List of timers with count."""
    items: list[TimerResponse]
    count: int
