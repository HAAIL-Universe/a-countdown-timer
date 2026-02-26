from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer status enumeration."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETE = "complete"


class Timer(BaseModel):
    """Timer domain model."""
    id: UUID
    duration: int = Field(..., gt=0)
    elapsed_time: int = Field(default=0, ge=0)
    status: TimerStatus = Field(default=TimerStatus.IDLE)
    urgency_level: int = Field(default=0, ge=0, le=3)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TimerCreate(BaseModel):
    """Request model for creating a timer."""
    duration: int = Field(..., gt=0)


class TimerUpdate(BaseModel):
    """Request model for updating a timer."""
    duration: int = Field(..., gt=0)


class TimerResponse(BaseModel):
    """Response model for timer."""
    id: str
    duration: int
    elapsed_time: int
    status: str
    urgency_level: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
