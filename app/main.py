from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS, DATABASE_URL
from app.database import init_db, close_db
from app.routers import health, timers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown."""
    await init_db(DATABASE_URL)
    yield
    await close_db()


app = FastAPI(title="Countdown Timer API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(timers.router)
