from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer state enum."""
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    DONE = "DONE"


class Timer(BaseModel):
    """Database model for timer entity."""
    id: UUID
    duration: int = Field(..., gt=0, description="Duration in seconds")
    elapsed_time: int = Field(default=0, ge=0, description="Elapsed seconds")
    status: TimerStatus = Field(default=TimerStatus.IDLE)
    urgency_level: int = Field(default=0, ge=0, le=1)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateTimerRequest(BaseModel):
    """Request body for POST /api/v1/timers."""
    duration: int = Field(..., gt=0, description="Duration in seconds")


class TimerResponse(BaseModel):
    """API response shape for timer."""
    id: UUID
    duration: int
    elapsed_time: int
    status: TimerStatus
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
