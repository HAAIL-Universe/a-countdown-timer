import asyncpg
from app.config import DATABASE_URL

_pool: asyncpg.Pool | None = None


async def create_pool() -> asyncpg.Pool:
    """Create and initialize the asyncpg connection pool."""
    global _pool
    if _pool is not None:
        return _pool
    
    _pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=5,
        max_size=20,
        command_timeout=30,
    )
    return _pool


async def get_pool() -> asyncpg.Pool:
    """Get the initialized connection pool; create if not already exists."""
    if _pool is None:
        return await create_pool()
    return _pool


async def close_pool() -> None:
    """Close and cleanup the connection pool."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
