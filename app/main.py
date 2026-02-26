import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS, ENVIRONMENT
from app.database import close_db, init_db
from app.routers import health, timers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle: startup and shutdown."""
    await init_db()
    yield
    await close_db()


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

app.include_router(health.router)
app.include_router(timers.router, prefix="/api/v1")
