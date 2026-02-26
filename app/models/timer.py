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
    """Timer model for database and API."""
    id: UUID = Field(default_factory=lambda: None)
    duration: int
    elapsed_time: int = 0
    status: TimerStatus = TimerStatus.IDLE
    urgency_level: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class TimerCreateRequest(BaseModel):
    """Request model for creating a timer."""
    duration: int = Field(..., gt=0, description="Timer duration in seconds")


class TimerUpdateRequest(BaseModel):
    """Request model for updating timer duration."""
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
