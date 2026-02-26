import asyncpg
from app.config import get_settings

_pool: asyncpg.Pool | None = None


async def create_pool() -> asyncpg.Pool:
    """Create and return asyncpg connection pool."""
    global _pool
    settings = get_settings()
    _pool = await asyncpg.create_pool(settings.DATABASE_URL)
    return _pool


async def get_pool() -> asyncpg.Pool:
    """Get the initialized connection pool."""
    if _pool is None:
        raise RuntimeError("Pool not initialized. Call create_pool() first.")
    return _pool


async def close_pool() -> None:
    """Close the connection pool."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
