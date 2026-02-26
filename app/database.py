import asyncpg
from app.config import get_settings

_pool: asyncpg.Pool | None = None


async def create_pool() -> asyncpg.Pool:
    """Create and cache a PostgreSQL connection pool."""
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
    """Get the cached connection pool, creating it if needed."""
    global _pool
    if _pool is None:
        await create_pool()
    return _pool


async def close_pool() -> None:
    """Close and clear the connection pool."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
