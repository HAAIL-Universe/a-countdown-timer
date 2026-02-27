from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    database_url: str
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    def get_cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS_ORIGINS into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton accessor. Cached after first call."""
    return Settings()


# Module-level exports for implementation contract
_settings = get_settings()
DATABASE_URL: str = _settings.database_url
CORS_ORIGINS: list[str] = _settings.get_cors_origins_list()
