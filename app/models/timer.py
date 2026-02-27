from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer status values."""
    idle = "idle"
    running = "running"
    paused = "paused"
    complete = "complete"


class Timer(BaseModel):
    """Timer model for countdown tracking."""
    id: UUID | None = Field(default=None)
    duration: int = Field(gt=0, description="Duration in seconds")
    elapsed_time: int = Field(default=0, ge=0)
    status: TimerStatus = Field(default=TimerStatus.idle)
    urgency_level: int = Field(default=0, ge=0, le=3)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)

    class Config:
        """Pydantic config."""
        use_enum_values = False

    def progress_ratio(self) -> float:
        """Calculate progress as elapsed_time / duration."""
        if self.duration == 0:
            return 0.0
        return min(self.elapsed_time / self.duration, 1.0)

    def calculate_urgency_level(self) -> int:
        """Calculate urgency level from 0-3 based on progress."""
        ratio = self.progress_ratio()
        if ratio < 0.33:
            return 0
        elif ratio < 0.66:
            return 1
        elif ratio < 0.9:
            return 2
        else:
            return 3

    def color_stage(self) -> str:
        """Return color stage: green, yellow, or red."""
        ratio = self.progress_ratio()
        if ratio < 0.33:
            return "green"
        elif ratio < 0.66:
            return "yellow"
        else:
            return "red"


class TimerRequest(BaseModel):
    """Request model for creating/updating a timer."""
    duration: int = Field(gt=0, description="Duration in seconds")


class TimerResponse(BaseModel):
    """Response model for timer data."""
    id: UUID
    duration: int
    elapsed_time: int
    status: TimerStatus
    urgency_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        use_enum_values = False
