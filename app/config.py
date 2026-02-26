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
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    @property
    def cors_origins_list(self) -> list[str]:
        """Return CORS origins as a list, parsing comma-separated string if needed."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached Settings singleton."""
    return Settings()


# Module-level exports for direct access
DATABASE_URL = get_settings().database_url
CORS_ORIGINS = get_settings().cors_origins_list
