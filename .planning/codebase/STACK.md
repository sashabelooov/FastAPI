# STACK.md
<!-- last_mapped: 2026-05-10 -->

## Runtime & Language

- **Language**: Python 3.10 (pinned via `.python-version`)
- **Package manager**: uv (v-synced, `uv.lock` committed)
- **Entry point**: `uvicorn app.main:app` (production), `uv run uvicorn ...` (local)

## Framework

| Layer | Library | Version |
|-------|---------|---------|
| Web framework | FastAPI (standard) | >=0.136.1 |
| ASGI server | uvicorn | >=0.46.0 |
| Data validation | pydantic v2 | >=2.13.4 |
| Settings | pydantic-settings | >=2.14.1 |
| ORM | SQLAlchemy 2.x (async) | >=2.0.49 |
| DB driver | asyncpg (via DATABASE_URL scheme) | transitive |

## Database

- **Primary DB**: PostgreSQL 16 (alpine image in docker-compose)
- **Connection**: async via `sqlalchemy.ext.asyncio` + asyncpg driver
- **URL scheme**: `postgresql+asyncpg://`
- **Session factory**: `async_sessionmaker` in `app/db/session.py`

## Caching / Queuing

- **Redis 7** defined in `docker-compose.yml` (alpine image, port 6379)
- Not yet imported or used in application code — configured at infra level only

## Configuration

- Settings loaded from `.env` via pydantic-settings (`SettingsConfigDict(env_file=".env")`)
- `.env.example` documents all required vars
- `extra="ignore"` — unknown env vars silently dropped

## Key Configuration Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `APP_NAME` | str | FastAPI app title |
| `DEBUG` | bool | SQLAlchemy echo + FastAPI debug |
| `ALLOWED_ORIGINS` | list[str] | CORS allowed origins |
| `DATABASE_URL` | str | Async DB connection string |
| `SECRET_KEY` | str | JWT signing key |
| `ALGORITHM` | str | JWT algorithm (HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | JWT access token TTL |
| `REFRESH_TOKEN_EXPIRE_DAYS` | int | JWT refresh token TTL |

## Containerization

- **Dockerfile**: `python:3.10-slim`, installs uv via pip, deps cached before app code
- **docker-compose.yml**: 3 services — `api`, `db` (postgres), `redis`
- Health checks on both db and redis before api starts
- `postgres_data` volume for persistence
