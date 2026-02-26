import asyncpg
from typing import Optional

from app.config import get_settings


_pool: Optional[asyncpg.Pool] = None


async def create_pool() -> asyncpg.Pool:
    """Create and initialize the asyncpg connection pool."""
    global _pool
    if _pool is not None:
        return _pool
    settings = get_settings()
    _pool = await asyncpg.create_pool(
        settings.database_url,
        min_size=5,
        max_size=20,
        command_timeout=60,
    )
    return _pool


async def get_pool() -> asyncpg.Pool:
    """Get the active connection pool, or raise if not initialized."""
    if _pool is None:
        raise RuntimeError("Database pool not initialized. Call create_pool() first.")
    return _pool


async def close_pool() -> None:
    """Close the connection pool."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


class Database:
    """Backward-compatible Database wrapper for lifespan management."""

    def __init__(self):
        pass

    async def connect(self) -> None:
        """Initialize connection pool."""
        await create_pool()

    async def disconnect(self) -> None:
        """Close connection pool."""
        await close_pool()


db = Database()
