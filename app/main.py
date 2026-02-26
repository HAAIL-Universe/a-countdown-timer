import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg

from app.config import get_settings
from app.database import init_pool, close_pool, set_pool
from app.routers import health, timers


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage database pool lifecycle."""
    await init_pool()
    yield
    await close_pool()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Countdown Timer API",
        description="A retro countdown timer with color urgency feedback",
        version="1.0.0",
        lifespan=lifespan,
    )

    allowed_origins = [
        origin.strip()
        for origin in settings.cors_origins.split(",")
        if origin.strip()
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(timers.router)

    return app


app = create_app()
