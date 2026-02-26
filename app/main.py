from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS, ENVIRONMENT
from app.database import close_db, get_pool, init_db
from app.repos.timer_repo import TimerRepository
from app.routers import health, timers
from app.services.timer_service import TimerService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle: startup and shutdown."""
    await init_db()
    yield
    await close_db()


async def get_timer_service() -> TimerService:
    """Dependency: inject TimerService with repo."""
    pool = await get_pool()
    repo = TimerRepository(pool)
    return TimerService(repo)


app = FastAPI(
    title="Countdown Timer",
    description="A retro countdown timer with character animation and color shifts",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.dependency_overrides[TimerService] = get_timer_service

app.include_router(health.router)
app.include_router(timers.router)
