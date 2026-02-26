from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer status enumeration."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETE = "complete"


class Timer(BaseModel):
    """Internal Timer domain model."""
    id: UUID
    duration: int
    elapsed_time: int
    status: TimerStatus
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        use_enum_values = False


class TimerRequest(BaseModel):
    """Request model for creating/updating a timer."""
    duration: int = Field(..., gt=0, description="Timer duration in seconds")


class TimerResponse(BaseModel):
    """Response model for timer endpoints."""
    id: UUID
    duration: int
    elapsed_time: int
    status: str
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TimerListResponse(BaseModel):
    """Response model for listing timers."""
    timers: list[TimerResponse]
