import asyncpg
from typing import Optional
from contextlib import asynccontextmanager


class Database:
    """Database connection pool manager."""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        """Initialize connection pool."""
        self.pool = await asyncpg.create_pool(self.database_url)

    async def disconnect(self) -> None:
        """Close connection pool."""
        if self.pool:
            await self.pool.close()

    @asynccontextmanager
    async def acquire(self):
        """Acquire a connection from pool."""
        async with self.pool.acquire() as conn:
            yield conn

    async def execute(self, query: str, *args) -> None:
        """Execute a query without returning results."""
        async with self.acquire() as conn:
            await conn.execute(query, *args)

    async def fetch(self, query: str, *args) -> list:
        """Fetch multiple rows."""
        async with self.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args) -> Optional[dict]:
        """Fetch single row."""
        async with self.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args) -> Optional[any]:
        """Fetch single value."""
        async with self.acquire() as conn:
            return await conn.fetchval(query, *args)
</result>
