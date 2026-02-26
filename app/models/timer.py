from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TimerStatus(str, Enum):
    """Timer status enumeration."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETE = "complete"


class Timer(BaseModel):
    """Timer domain model."""
    id: UUID
    duration: int
    elapsed_time: int
    status: TimerStatus
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    @field_validator("duration")
    @classmethod
    def duration_positive(cls, v: int) -> int:
        """Duration must be positive."""
        if v <= 0:
            raise ValueError("duration must be positive")
        return v

    @field_validator("elapsed_time")
    @classmethod
    def elapsed_time_non_negative(cls, v: int) -> int:
        """Elapsed time must be non-negative."""
        if v < 0:
            raise ValueError("elapsed_time must be non-negative")
        return v

    @field_validator("urgency_level")
    @classmethod
    def urgency_level_valid(cls, v: int) -> int:
        """Urgency level must be 0-3."""
        if v < 0 or v > 3:
            raise ValueError("urgency_level must be 0-3")
        return v


class TimerCreate(BaseModel):
    """Timer creation request."""
    duration: int = Field(..., gt=0)


class TimerUpdate(BaseModel):
    """Timer update request."""
    duration: Optional[int] = Field(None, gt=0)


class TimerResponse(BaseModel):
    """Timer API response."""
    id: UUID
    duration: int
    elapsed_time: int
    status: TimerStatus
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True
