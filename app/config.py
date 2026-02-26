import os

DATABASE_URL: str = os.getenv("DATABASE_URL", "")
CORS_ORIGINS: list[str] = [
    origin.strip() for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]
