from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer state enumeration."""
    idle = "idle"
    running = "running"
    paused = "paused"
    complete = "complete"


class Timer(BaseModel):
    """Timer domain model — persisted to DB."""
    id: UUID
    duration: int = Field(..., gt=0, description="Duration in seconds")
    elapsed_time: int = Field(default=0, ge=0, description="Elapsed time in seconds")
    status: TimerStatus = Field(default=TimerStatus.idle)
    urgency_level: int = Field(default=0, ge=0, le=3)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateTimerRequest(BaseModel):
    """Request body for POST /api/v1/timers (create)."""
    duration: int = Field(..., gt=0, description="Duration in seconds")


class TimerResponse(BaseModel):
    """Response body for timer endpoints."""
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
    """Response body for GET /api/v1/timers."""
    items: list[TimerResponse]
    count: int
