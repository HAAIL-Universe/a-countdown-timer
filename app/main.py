from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import create_pool, close_pool
from app.routers import health, timers

settings = get_settings()

app = FastAPI(title="A countdown timer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(timers.router, prefix="/api/v1/timers")


@app.on_event("startup")
async def startup() -> None:
    """Initialize database pool on app startup."""
    await create_pool()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Close database pool on app shutdown."""
    await close_pool()
