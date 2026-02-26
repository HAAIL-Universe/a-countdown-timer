import asyncio
from typing import AsyncGenerator
import asyncpg
from contextlib import asynccontextmanager
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/countdown_timer")

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    """Get or create the database connection pool."""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=5, max_size=20)
    return _pool


async def close_pool() -> None:
    """Close the database connection pool."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


@asynccontextmanager
async def get_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """Get a connection from the pool."""
    pool = await get_pool()
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)


async def init_db() -> None:
    """Initialize the database schema."""
    async with get_connection() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS timers (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                duration INTEGER NOT NULL,
                elapsed_time INTEGER NOT NULL DEFAULT 0,
                status VARCHAR(255) NOT NULL DEFAULT 'idle',
                urgency_level INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """
        )


async def cleanup_db() -> None:
    """Cleanup database resources."""
    await close_pool()
