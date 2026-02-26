from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import create_pool, close_pool
from app.routers import health, timers

app = FastAPI(title="Countdown Timer API", version="1.0.0")

settings = get_settings()


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize database pool on startup."""
    await create_pool()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Close database pool on shutdown."""
    await close_pool()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(timers.router)
