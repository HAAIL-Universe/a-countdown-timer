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
    cors_origins: str = "http://localhost:5173,http://localhost:3000"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


DATABASE_URL: str = ""
CORS_ORIGINS: list[str] = []


def _init_module_exports() -> None:
    """Initialize module-level exports from settings."""
    global DATABASE_URL, CORS_ORIGINS
    settings = get_settings()
    DATABASE_URL = settings.database_url
    CORS_ORIGINS = settings.cors_origins.split(",")


_init_module_exports()
