from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TimerStatus(str, Enum):
    """Timer status values."""
    idle = "idle"
    running = "running"
    paused = "paused"
    complete = "complete"


class Timer(BaseModel):
    """Timer domain model."""
    id: UUID | None = Field(default=None)
    duration: int = Field(gt=0, description="Duration in seconds")
    elapsed_time: int = Field(default=0, ge=0, description="Elapsed time in seconds")
    status: TimerStatus = Field(default=TimerStatus.idle)
    urgency_level: int = Field(default=0, ge=0, le=3)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)

    @field_validator("elapsed_time")
    @classmethod
    def elapsed_time_not_exceeds_duration(cls, v: int, info) -> int:
        """Ensure elapsed_time does not exceed duration."""
        if "duration" in info.data and v > info.data["duration"]:
            raise ValueError("elapsed_time cannot exceed duration")
        return v

    def calculate_urgency_level(self) -> int:
        """Calculate urgency level based on elapsed_time / duration ratio."""
        if self.duration <= 0:
            return 0
        ratio = self.elapsed_time / self.duration
        if ratio < 0.33:
            return 0
        elif ratio < 0.66:
            return 1
        elif ratio < 0.90:
            return 2
        else:
            return 3

    def get_color(self) -> Literal["green", "yellow", "red"]:
        """Get color based on urgency level."""
        urgency = self.calculate_urgency_level()
        if urgency == 0:
            return "green"
        elif urgency <= 2:
            return "yellow"
        else:
            return "red"


class TimerCreate(BaseModel):
    """Request model for creating a timer."""
    duration: int = Field(gt=0, description="Duration in seconds")


class TimerUpdate(BaseModel):
    """Request model for updating a timer."""
    duration: int = Field(gt=0, description="Duration in seconds")


class TimerResponse(BaseModel):
    """Response model for timer."""
    id: UUID
    duration: int
    elapsed_time: int
    status: TimerStatus
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
