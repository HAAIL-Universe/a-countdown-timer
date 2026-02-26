from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import create_pool, close_pool
from app.routers import health, timers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage database pool lifecycle on app startup/shutdown."""
    await create_pool()
    yield
    await close_pool()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Countdown Timer API",
        description="A simple countdown timer REST API",
        version="1.0.0",
        lifespan=lifespan,
    )

    settings = get_settings()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(timers.router)

    return app


app = create_app()
