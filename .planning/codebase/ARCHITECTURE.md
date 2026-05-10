# ARCHITECTURE.md
<!-- last_mapped: 2026-05-10 -->

## Pattern

**Layered FastAPI application** with async-first design. The directory structure follows a conventional separation into:

```
Request → Router (api/) → Service (services/) → Repository (repository/) → DB
                         ↓
                     Schema (schemas/) ← Pydantic validation
```

All layers are scaffolded (directories exist) but only the foundation is implemented.

## Implemented Layers

### Core (`app/core/`)
- `config.py` — pydantic-settings `Settings` class, singleton `settings` object
- `dependencies.py` — FastAPI dependency injection; provides `get_db()` async generator yielding `AsyncSession`

### Database (`app/db/`)
- `base.py` — SQLAlchemy `DeclarativeBase` + abstract `TimeStampedBase` (UUID PK, created_at, updated_at)
- `session.py` — `create_async_engine` + `async_sessionmaker` → `AsyncSessionLocal`

### Application (`app/main.py`)
- FastAPI app instantiation with `lifespan` context manager (disposes engine on shutdown)
- CORS middleware wired from `settings.allowed_origins`
- One endpoint: `GET /` health check

## Empty / Scaffolded Layers

| Directory | Purpose | Status |
|-----------|---------|--------|
| `app/api/` | Route handlers / routers | Empty |
| `app/models/` | SQLAlchemy ORM models | Empty |
| `app/repository/` | DB access layer | Empty |
| `app/schemas/` | Pydantic request/response schemas | Empty |
| `app/services/` | Business logic | Empty |

## Data Flow

```
FastAPI Request
    ↓
app/main.py (middleware + routing)
    ↓
app/api/ (routers — not yet implemented)
    ↓
app/services/ (business logic — not yet implemented)
    ↓
app/repository/ (DB queries — not yet implemented)
    ↓
app/db/session.py (AsyncSession via get_db dependency)
    ↓
PostgreSQL
```

## Entry Points

- `app.main:app` — ASGI app (uvicorn target)
- `main.py` (root) — stub `main()`, not connected to FastAPI app

## Async Strategy

- All DB operations use `sqlalchemy.ext.asyncio` (`AsyncSession`, `async_sessionmaker`, `create_async_engine`)
- FastAPI routes designed to be `async def`
- Engine disposed cleanly via lifespan `asynccontextmanager`

## Auth Architecture (planned)

JWT settings are fully configured but no auth middleware, decorators, or routes exist yet. Will likely use `app/core/dependencies.py` to add `get_current_user` dependency.
