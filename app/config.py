from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    database_url: str
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    @property
    def DATABASE_URL(self) -> str:
        """Exported as DATABASE_URL per contract."""
        return self.database_url

    @property
    def CORS_ORIGINS(self) -> list[str]:
        """Exported as CORS_ORIGINS per contract."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton accessor for application settings."""
    return Settings()
