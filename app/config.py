import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""

    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/countdown_timer")
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = environment == "development"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
