from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # --- Database ---
    database_url: str
    
    # --- CORS ---
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    @property
    def DATABASE_URL(self) -> str:
        """Exported constant for backward compatibility."""
        return self.database_url

    @property
    def CORS_ORIGINS(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton accessor. Cached after first call."""
    return Settings()
