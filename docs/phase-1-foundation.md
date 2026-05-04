# Phase 1 — Foundation

## What we built
Project skeleton: configuration, database connection, base model, and the FastAPI entry point.

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

## Key decisions

| Decision | Reason |
|----------|--------|
| UUID primary keys | Globally unique, safe to expose in URLs, no sequential ID guessing |
| `TimeStampedBase` abstract class | DRY — every table gets `id`, `created_at`, `updated_at` without repeating columns |
| Pydantic settings | SSOT — one place for all config, typed, validated on startup |
| Async SQLAlchemy | Non-blocking I/O — one slow DB query doesn't block other requests |
| `get_db` as a dependency | SoC — routes don't manage sessions directly, the dependency does |
| `lifespan` handler | Proper connection pool cleanup on shutdown, avoids connection leaks |

## Principles applied
- **SSOT** — all config lives in `config.py`, sourced from `.env`
- **DRY** — `TimeStampedBase` avoids repeating timestamp columns in every model
- **SoC** — config, database infrastructure, and app wiring are in separate files
- **Defensive Programming** — `get_db` uses `async with` so sessions always close even on errors
- **YAGNI** — no extra fields or endpoints added speculatively
