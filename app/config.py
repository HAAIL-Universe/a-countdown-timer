from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    database_url: str = "postgresql://localhost/countdown_timer"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Return application settings instance."""
    return Settings()


settings = get_settings()
