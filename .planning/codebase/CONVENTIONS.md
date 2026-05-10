# CONVENTIONS.md
<!-- last_mapped: 2026-05-10 -->

## Code Style

- Python 3.10+ syntax (union types via `|` available, but not observed yet)
- `from __future__ import annotations` used in db and config modules for forward-ref support
- Type hints used throughout (SQLAlchemy `Mapped[T]`, pydantic field types, return annotations)
- No linting config found (no `ruff.toml`, `.flake8`, `mypy.ini`) — Pylance type checking enabled via VSCode settings

## Naming

| Entity | Convention | Example |
|--------|-----------|---------|
| Files | `snake_case.py` | `config.py`, `session.py` |
| Classes | `PascalCase` | `Settings`, `TimeStampedBase` |
| Functions/methods | `snake_case` | `get_db()`, `health_check()` |
| Variables | `snake_case` | `engine`, `settings` |
| Constants/singletons | `snake_case` at module level | `settings`, `engine`, `AsyncSessionLocal` |
| Env variables | `UPPER_SNAKE_CASE` | `DATABASE_URL`, `SECRET_KEY` |

## FastAPI Patterns

- Async route handlers (`async def`)
- Lifespan context manager for startup/shutdown (not deprecated `on_event`)
- Return type annotations on routes (e.g., `-> dict[str, str]`)
- Dependency injection via `Depends()` (implemented in `dependencies.py`)

## SQLAlchemy Patterns

- SQLAlchemy 2.x style with `Mapped[T]` and `mapped_column()`
- `DeclarativeBase` subclassed in `app/db/base.py`
- Abstract mixin `TimeStampedBase` for shared fields (UUID PK, timestamps)
- UUID primary keys (`uuid.UUID`, PostgreSQL `UUID(as_uuid=True)`)
- Server-side timestamps via `func.now()` (not Python-side datetime)
- `expire_on_commit=False` on session — prevents lazy-load errors after commit

## Pydantic Patterns

- v2 style (`BaseSettings`, `SettingsConfigDict`)
- `extra="ignore"` on settings — silently ignores unknown env vars
- No `model_validator` or custom validators observed yet

## Error Handling

- No custom error handling implemented yet
- FastAPI's default exception handlers in place

## Dependency Injection

- `get_db()` — yields `AsyncSession`, used as `Depends(get_db)` in route handlers
- Pattern: `async with AsyncSessionLocal() as session: yield session`
