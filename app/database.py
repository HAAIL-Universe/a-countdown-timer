import asyncpg
import os

_pool: asyncpg.Pool | None = None


async def create_pool() -> asyncpg.Pool:
    """Initialize and return the asyncpg connection pool."""
    global _pool
    if _pool is not None:
        return _pool
    
    _pool = await asyncpg.create_pool(
        os.getenv("DATABASE_URL", ""),
        min_size=10,
        max_size=20,
        command_timeout=60,
    )
    return _pool


async def get_pool() -> asyncpg.Pool:
    """Retrieve the global connection pool; create if missing."""
    if _pool is None:
        return await create_pool()
    return _pool


async def close_pool() -> None:
    """Close the connection pool and reset global reference."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
