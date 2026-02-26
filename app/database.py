import asyncpg
from typing import Optional
from app.config import settings


class Database:
    """Manages PostgreSQL connection pool."""

    def __init__(self) -> None:
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        """Initialize connection pool."""
        self.pool = await asyncpg.create_pool(
            settings.database_url,
            min_size=10,
            max_size=20,
            command_timeout=60,
        )

    async def disconnect(self) -> None:
        """Close connection pool."""
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args) -> None:
        """Execute a query without returning results."""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)

    async def fetch(self, query: str, *args) -> list:
        """Fetch multiple rows."""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """Fetch single row."""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args) -> Optional:
        """Fetch single value."""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)


db = Database()
