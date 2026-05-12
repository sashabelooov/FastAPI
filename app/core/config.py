from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str
    debug: bool
    allowed_origins: list[str] = Field(default_factory=list, env="ALLOWED_ORIGINS")
    allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    allow_methods: list[str] = Field(default_factory=lambda: ["*"], env="CORS_ALLOW_METHODS")
    allow_headers: list[str] = Field(default_factory=lambda: ["*"], env="CORS_ALLOW_HEADERS")

    database_url: str
    redis_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

settings = Settings()