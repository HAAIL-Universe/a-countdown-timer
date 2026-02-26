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
        if v <= 0:
            raise ValueError("duration must be a positive integer")
        return v

    @field_validator("elapsed_time")
    @classmethod
    def elapsed_time_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("elapsed_time must be non-negative")
        return v

    @field_validator("urgency_level")
    @classmethod
    def urgency_level_valid(cls, v: int) -> int:
        if v not in (0, 1, 2, 3):
            raise ValueError("urgency_level must be 0, 1, 2, or 3")
        return v

    class Config:
        use_enum_values = False


class TimerCreate(BaseModel):
    """Request payload for creating a timer."""
    duration: int = Field(..., gt=0, description="Timer duration in seconds")

    class Config:
        use_enum_values = False


class TimerUpdate(BaseModel):
    """Request payload for updating timer duration."""
    duration: int = Field(..., gt=0, description="Timer duration in seconds")

    class Config:
        use_enum_values = False


class TimerResponse(BaseModel):
    """Response payload for timer endpoints."""
    id: UUID
    duration: int
    elapsed_time: int
    status: TimerStatus
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        use_enum_values = False


class TimerListResponse(BaseModel):
    """Response payload for listing timers."""
    timers: list[TimerResponse]

    class Config:
        use_enum_values = False
