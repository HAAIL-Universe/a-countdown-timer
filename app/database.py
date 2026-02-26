import asyncpg
from app.config import get_settings

_pool: asyncpg.Pool | None = None


async def create_pool() -> asyncpg.Pool:
    """Initialize and return the asyncpg connection pool."""
    global _pool
    if _pool is not None:
        return _pool
    
    settings = get_settings()
    _pool = await asyncpg.create_pool(
        settings.DATABASE_URL,
        min_size=5,
        max_size=20,
    )
    return _pool


async def get_pool() -> asyncpg.Pool:
    """Get the current connection pool (must be initialized via create_pool first)."""
    global _pool
    if _pool is None:
        raise RuntimeError("Database pool not initialized. Call create_pool() first.")
    return _pool


async def close_pool() -> None:
    """Close the connection pool and clean up resources."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
