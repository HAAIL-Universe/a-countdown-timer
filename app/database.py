import asyncpg
from typing import Optional
from contextlib import asynccontextmanager

_pool: Optional[asyncpg.Pool] = None


async def init_db(database_url: str) -> None:
    """Initialize database connection pool."""
    global _pool
    _pool = await asyncpg.create_pool(database_url, min_size=5, max_size=20)


async def close_db() -> None:
    """Close database connection pool."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def get_db() -> asyncpg.Connection:
    """Get a database connection from the pool."""
    global _pool
    if _pool is None:
        raise RuntimeError("Database pool not initialized")
    async with _pool.acquire() as conn:
        yield conn


@asynccontextmanager
async def get_connection():
    """Context manager for acquiring a database connection."""
    global _pool
    if _pool is None:
        raise RuntimeError("Database pool not initialized")
    async with _pool.acquire() as conn:
        yield conn
