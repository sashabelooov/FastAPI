# Phase 1b — Infrastructure

## What we built
Alembic migrations, Docker setup, and test foundation.

## File creation order

### 1. `migrations/` (via `alembic init migrations`)
Scaffolded by Alembic. Creates the `migrations/` folder and `alembic.ini`.

### 2. `alembic.ini`
Cleared `sqlalchemy.url` — value is set programmatically from `settings` in `env.py`.

### 3. `migrations/env.py`
Configured Alembic for async SQLAlchemy:
- Pulls `DATABASE_URL` from `settings` (SSOT)
- Sets `target_metadata = Base.metadata` so Alembic can detect model changes
- Uses `asyncio.run()` + `async_engine_from_config` for async support
- Uses `NullPool` during migrations (no connection reuse)

### 4. `Dockerfile`
Single-stage build using `python:3.10-slim`:
- Installs `uv` via pip
- Copies `pyproject.toml` + `uv.lock` first for Docker layer caching
- Runs `uv sync --frozen --no-dev` (exact versions, no dev deps in production)
- Starts app with `uvicorn` on port 8000

### 5. `docker-compose.yml`
Three services:
- `api` — FastAPI app, waits for `db` and `redis` to be healthy before starting
- `db` — PostgreSQL 16 Alpine, health-checked, data persisted in a named volume
- `redis` — Redis 7 Alpine, health-checked
- Overrides `DATABASE_URL` for Docker networking (`db` host instead of `localhost`)

### 6. `.dockerignore`
Excludes `.venv/`, `.env`, `.git/`, `__pycache__/` from the Docker build context.

### 7. `pytest.ini`
Sets `asyncio_mode = auto` — all async test functions run automatically without needing `@pytest.mark.asyncio` on each one.

### 8. `test/__init__.py`
Empty file — makes `test/` a Python package so pytest can import from it.

### 9. `test/conftest.py`
Contains the `client` fixture: an `AsyncClient` with `ASGITransport` that makes real HTTP requests to the app without a running server.

### 10. `test/test_health.py`
First test: verifies `GET /` returns `200 OK` with the correct JSON body.

## Key decisions

| Decision | Reason |
|----------|--------|
| `alembic.ini` has empty `sqlalchemy.url` | SSOT — URL lives in `.env` via `settings`, not duplicated in alembic config |
| `NullPool` in migrations | Migrations are one-shot scripts, not long-running apps — no need for connection pooling |
| Docker layer order: deps before app code | If only app code changes, Docker reuses the cached dependency layer — faster rebuilds |
| `depends_on` with `service_healthy` | API waits for PostgreSQL to be truly ready, not just started — prevents startup race condition |
| `DATABASE_URL` overridden in compose | Inside Docker, db host is `db` (service name), not `localhost` — local `.env` stays unchanged |
| `asyncio_mode = auto` in pytest.ini | DRY — no need to decorate every async test with `@pytest.mark.asyncio` |
| `ASGITransport` in test client | Tests hit the real app without a running server — fast, isolated, no port conflicts |

## Principles applied
- **SSOT** — database URL defined once in `.env`, reused by both Alembic and Docker
- **DRY** — `asyncio_mode = auto` removes boilerplate from every test file
- **Defensive Programming** — healthchecks ensure services are actually ready before the API starts
- **SoC** — fixtures in `conftest.py`, tests in `test_*.py`
- **YAGNI** — no extra test utilities added until needed

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
