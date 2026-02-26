import asyncpg
from typing import Optional
import os


class Database:
    """PostgreSQL connection pool manager."""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        """Initialize connection pool."""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=5,
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

    async def fetch_one(self, query: str, *args) -> Optional[dict]:
        """Fetch a single row as a dict."""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None

    async def fetch_all(self, query: str, *args) -> list[dict]:
        """Fetch all rows as list of dicts."""
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]


def get_database(database_url: Optional[str] = None) -> Database:
    """Factory function to create Database instance."""
    url = database_url or os.getenv("DATABASE_URL")
    if not url:
        url = "postgresql://localhost/countdown_timer"
    return Database(url)
