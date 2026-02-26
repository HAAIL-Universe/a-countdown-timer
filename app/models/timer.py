from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer status enumeration."""
    idle = "idle"
    running = "running"
    paused = "paused"
    complete = "complete"


class Timer(BaseModel):
    """Timer model for database and API."""
    id: UUID
    duration: int
    elapsed_time: int = 0
    status: TimerStatus = TimerStatus.idle
    urgency_level: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateTimerRequest(BaseModel):
    """Request model for creating a timer."""
    duration: int = Field(..., gt=0, description="Timer duration in seconds")


class TimerResponse(BaseModel):
    """Response model for timer endpoints."""
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
