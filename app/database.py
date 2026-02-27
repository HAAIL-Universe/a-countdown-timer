import asyncpg
from typing import AsyncGenerator
from contextlib import asynccontextmanager
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/countdown_timer")

_pool: asyncpg.Pool | None = None


async def init_db() -> None:
    """Initialize database connection pool."""
    global _pool
    _pool = await asyncpg.create_pool(DATABASE_URL, min_size=5, max_size=20)


async def close_db() -> None:
    """Close database connection pool."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """Get a database connection from the pool."""
    global _pool
    if not _pool:
        raise RuntimeError("Database not initialized")
    async with _pool.acquire() as conn:
        yield conn


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[asyncpg.Connection, None]:
    """Context manager for database connections."""
    global _pool
    if not _pool:
        raise RuntimeError("Database not initialized")
    async with _pool.acquire() as conn:
        yield conn
