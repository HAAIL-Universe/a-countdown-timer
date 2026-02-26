from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""
    database_url: str = "postgresql://localhost/countdown_timer"
    cors_origins: str = "http://localhost:5173,http://localhost:8000"
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


DATABASE_URL = get_settings().database_url
CORS_ORIGINS = [origin.strip() for origin in get_settings().cors_origins.split(",")]
ENVIRONMENT = get_settings().environment
