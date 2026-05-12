from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.database.session import AsyncSessionLocal, engine, redis_client

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await engine.dispose()
    await redis_client.aclose()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)


app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/health")
async def health_check() -> dict:
    services: dict[str, str] = {}

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        services["database"] = "ok"
    except Exception as exc:
        services["database"] = f"error: {exc}"

    try:
        await redis_client.ping()
        services["redis"] = "ok"
    except Exception as exc:
        services["redis"] = f"error: {exc}"

    overall = "ok" if all(v == "ok" for v in services.values()) else "degraded"

    return {
        "status": overall,
        "version": app.version,
        "services": services,
    }