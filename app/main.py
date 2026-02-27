import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS
from app.database import create_pool, close_pool
from app.routers.health import router as health_router
from app.routers.timers import router as timers_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup/shutdown: create and close the DB pool."""
    await create_pool()
    yield
    await close_pool()


app = FastAPI(
    title="Countdown Timer API",
    version="1.0.0",
    description="A countdown timer that displays urgency via color changes and animated facial expressions.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(timers_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
