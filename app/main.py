from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import close_pool, create_pool, get_pool
from app.repos.timer_repo import TimerRepo
from app.routers import health, timers
from app.services.timer_service import TimerService


async def get_timer_service() -> TimerService:
    """Dependency: Provide TimerService with initialized pool."""
    pool = await get_pool()
    repo = TimerRepo(pool)
    return TimerService(repo)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    await create_pool()
    yield
    await close_pool()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="Timer API",
        description="A countdown timer service",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(health.router)
    app.include_router(timers.router, dependencies=[Depends(get_timer_service)])
    
    return app


app = create_app()
