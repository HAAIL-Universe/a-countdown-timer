from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import create_pool, close_pool
from app.routers import health, timers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle: pool startup and shutdown."""
    await create_pool()
    yield
    await close_pool()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Countdown Timer API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins_list(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(timers.router, prefix="/api/v1/timers")

    return app


app = create_app()
