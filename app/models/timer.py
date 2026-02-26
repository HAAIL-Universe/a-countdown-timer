from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer operational status."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETE = "complete"


class Timer(BaseModel):
    """Database timer model."""
    id: UUID
    duration: int
    elapsed_time: int
    status: TimerStatus
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TimerCreateRequest(BaseModel):
    """Request body for creating a timer."""
    duration: int = Field(..., gt=0, description="Duration in seconds")


class TimerUpdateRequest(BaseModel):
    """Request body for updating timer duration."""
    duration: int = Field(..., gt=0, description="Duration in seconds")


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
