# STRUCTURE.md
<!-- last_mapped: 2026-05-10 -->

## Directory Layout

```
/
├── app/                        # Application package
│   ├── __init__.py
│   ├── main.py                 # FastAPI app, CORS, lifespan
│   ├── api/                    # Route handlers (empty)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # pydantic-settings Settings class
│   │   └── dependencies.py     # FastAPI dependency: get_db()
│   ├── db/
│   │   ├── base.py             # DeclarativeBase, TimeStampedBase
│   │   └── session.py          # engine, AsyncSessionLocal
│   ├── models/                 # SQLAlchemy ORM models (empty)
│   ├── repository/             # DB access layer (empty)
│   ├── schemas/                # Pydantic schemas (empty)
│   └── services/               # Business logic (empty)
├── test/                       # Test directory (empty)
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI pipeline (empty)
│       └── cd.yml              # CD pipeline (empty)
├── .planning/                  # GSD planning artifacts
│   └── codebase/               # This codebase map
├── .venv/                      # Virtual environment (uv-managed)
├── .vscode/
│   └── settings.json           # Python interpreter path
├── .env                        # Local secrets (gitignored)
├── .env.example                # Env var documentation
├── .gitignore
├── .python-version             # 3.10 (pyenv/uv pin)
├── docker-compose.yml          # api + db + redis services
├── Dockerfile                  # Production image
├── main.py                     # Root stub (not connected to app)
├── pyproject.toml              # Project metadata + dependencies
├── README.md                   # Empty
└── uv.lock                     # Lockfile (committed)
```

## Key Locations

| What | Where |
|------|-------|
| App entry point | `app/main.py` — `app = FastAPI(...)` |
| Settings singleton | `app/core/config.py` — `settings = Settings()` |
| DB session factory | `app/db/session.py` — `AsyncSessionLocal` |
| Base ORM model | `app/db/base.py` — `TimeStampedBase` |
| DB dependency | `app/core/dependencies.py` — `get_db()` |

## Naming Conventions

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase` (e.g., `Settings`, `TimeStampedBase`)
- **Variables/functions**: `snake_case`
- **Env vars**: `UPPER_SNAKE_CASE`
- **Docker services**: lowercase (`api`, `db`, `redis`)

## Import Patterns

- Absolute imports from `app.*` package
- `from __future__ import annotations` used in `db/base.py`, `db/session.py`, `core/config.py`
- Settings accessed as singleton: `from app.core.config import settings`
