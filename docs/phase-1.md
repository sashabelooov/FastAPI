# Phase 1 — Foundation & Infrastructure

## What we built
Project skeleton: configuration, database connection, base model, FastAPI entry point, Alembic migrations, Docker setup, and test foundation.

## File creation order

### 1. `.env`
Stores all environment-specific secrets and config values. Never committed to git.
Key values: `APP_NAME`, `DEBUG`, `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, token expiry settings.

### 2. `.env.example`
A safe copy of `.env` with placeholder values. Committed to git so future developers know what variables are required.

### 3. `app/core/config.py`
Pydantic `Settings` class that reads `.env` into typed Python attributes.
Single source of truth for all config — no hardcoded values anywhere else in the codebase.

### 4. `app/db/base.py`
Defines `Base` (SQLAlchemy `DeclarativeBase`) and `TimeStampedBase` (abstract model with `id`, `created_at`, `updated_at`).
Every model in the project inherits from `TimeStampedBase` to get these fields for free.

### 5. `app/db/session.py`
Creates the async SQLAlchemy `engine` and `AsyncSessionLocal` session factory.
Used by `get_db` to create per-request database sessions.

### 6. `app/core/dependencies.py`
Contains `get_db` — an async generator that yields a database session and closes it after each request.
Injected into route handlers via FastAPI's dependency injection system.

### 7. `app/main.py`
FastAPI application instance with:
- `lifespan` context manager (disposes engine on shutdown)
- CORS middleware
- `GET /` health check endpoint

### 8. `migrations/` (via `alembic init migrations`)
Scaffolded by Alembic. Creates the `migrations/` folder and `alembic.ini`.

### 9. `alembic.ini`
Cleared `sqlalchemy.url` — value is set programmatically from `settings` in `env.py`.

### 10. `migrations/env.py`
Configured Alembic for async SQLAlchemy:
- Pulls `DATABASE_URL` from `settings` (SSOT)
- Sets `target_metadata = Base.metadata` so Alembic can detect model changes
- Uses `asyncio.run()` + `async_engine_from_config` for async support
- Uses `NullPool` during migrations (no connection reuse)

### 11. `Dockerfile`
Single-stage build using `python:3.10-slim`:
- Installs `uv` via pip
- Copies `pyproject.toml` + `uv.lock` first for Docker layer caching
- Runs `uv sync --frozen --no-dev` (exact versions, no dev deps in production)
- Starts app with `uvicorn` on port 8000

### 12. `docker-compose.yml`
Three services:
- `api` — FastAPI app, waits for `db` and `redis` to be healthy before starting
- `db` — PostgreSQL 16 Alpine, health-checked, data persisted in a named volume
- `redis` — Redis 7 Alpine, health-checked
- Overrides `DATABASE_URL` for Docker networking (`db` host instead of `localhost`)

### 13. `.dockerignore`
Excludes `.venv/`, `.env`, `.git/`, `__pycache__/` from the Docker build context.

### 14. `pytest.ini`
Sets `asyncio_mode = auto` — all async test functions run automatically without needing `@pytest.mark.asyncio` on each one.

### 15. `test/__init__.py`
Empty file — makes `test/` a Python package so pytest can import from it.

### 16. `test/conftest.py`
Contains the `client` fixture: an `AsyncClient` with `ASGITransport` that makes real HTTP requests to the app without a running server.

### 17. `test/test_health.py`
First test: verifies `GET /` returns `200 OK` with the correct JSON body.

## Key decisions

| Decision | Reason |
|----------|--------|
| UUID primary keys | Globally unique, safe to expose in URLs, no sequential ID guessing |
| `TimeStampedBase` abstract class | DRY — every table gets `id`, `created_at`, `updated_at` without repeating columns |
| Pydantic settings | SSOT — one place for all config, typed, validated on startup |
| Async SQLAlchemy | Non-blocking I/O — one slow DB query doesn't block other requests |
| `get_db` as a dependency | SoC — routes don't manage sessions directly, the dependency does |
| `lifespan` handler | Proper connection pool cleanup on shutdown, avoids connection leaks |
| `alembic.ini` has empty `sqlalchemy.url` | SSOT — URL lives in `.env` via `settings`, not duplicated in alembic config |
| `NullPool` in migrations | Migrations are one-shot scripts, not long-running apps — no need for connection pooling |
| Docker layer order: deps before app code | If only app code changes, Docker reuses the cached dependency layer — faster rebuilds |
| `depends_on` with `service_healthy` | API waits for PostgreSQL to be truly ready, not just started — prevents startup race condition |
| `DATABASE_URL` overridden in compose | Inside Docker, db host is `db` (service name), not `localhost` — local `.env` stays unchanged |
| `asyncio_mode = auto` in pytest.ini | DRY — no need to decorate every async test with `@pytest.mark.asyncio` |
| `ASGITransport` in test client | Tests hit the real app without a running server — fast, isolated, no port conflicts |

## Principles applied
- **SSOT** — all config in `.env`, one `Settings` class, reused by app, Alembic, and Docker
- **DRY** — `TimeStampedBase` and `asyncio_mode = auto` eliminate repetition
- **SoC** — config, db infrastructure, app wiring, and tests are fully separated
- **Defensive Programming** — `get_db` closes sessions on error; healthchecks prevent race conditions
- **YAGNI** — no extra fields, endpoints, or utilities added speculatively

## Useful commands

| Command | What it does |
|---------|-------------|
| `docker compose up` | Start all services |
| `docker compose up --build` | Rebuild image and start |
| `docker compose down` | Stop and remove containers |
| `docker compose down -v` | Stop and delete volumes (wipes DB data) |
| `uv run alembic upgrade head` | Apply all pending migrations |
| `uv run alembic revision --autogenerate -m "message"` | Generate a new migration from model changes |
| `uv run alembic downgrade -1` | Roll back the last migration |
| `uv run pytest test/ -v` | Run all tests |
