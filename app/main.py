from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.app_name
    }