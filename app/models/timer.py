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
    """Timer domain model."""
    id: Optional[UUID] = Field(default=None)
    duration: int = Field(gt=0, description="Duration in seconds")
    elapsed_time: int = Field(default=0, ge=0, description="Elapsed time in seconds")
    status: TimerStatus = Field(default=TimerStatus.IDLE)
    urgency_level: int = Field(default=0, ge=0, le=3)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""
        use_enum_values = False


class TimerCreate(BaseModel):
    """Request model for creating a timer."""
    duration: int = Field(gt=0, description="Duration in seconds")


class TimerUpdate(BaseModel):
    """Request model for updating a timer."""
    duration: Optional[int] = Field(default=None, gt=0)
    elapsed_time: Optional[int] = Field(default=None, ge=0)
    status: Optional[TimerStatus] = None


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
        """Pydantic configuration."""
        use_enum_values = False


TimerCreateRequest = TimerCreate
