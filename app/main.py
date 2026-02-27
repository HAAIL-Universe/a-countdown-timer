import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import DatabasePool
from app.routers import health, timers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    await DatabasePool.initialize()
    yield
    await DatabasePool.close()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="Countdown Timer API",
        version="1.0.0",
        lifespan=lifespan
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(health.router)
    app.include_router(timers.router)
    
    return app


app = create_app()
