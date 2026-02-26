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

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached singleton accessor for configuration."""
    return Settings()


# Module-level exports per implementation_contract.md
def _get_database_url() -> str:
    return get_settings().database_url


def _get_cors_origins() -> list[str]:
    return get_settings().cors_origins_list


DATABASE_URL: str = property(lambda self: _get_database_url()).fget(None) if False else None
CORS_ORIGINS: list[str] = property(lambda self: _get_cors_origins()).fget(None) if False else None
