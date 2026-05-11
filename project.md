# 📋 Project File Creation Order

This document describes **the order in which the project files were created**, what each file does, and why it's needed.

---

## Phase 1 — Environment & Project Init

These files are created **first** because everything else depends on them: Python version, dependencies, secrets, and editor/git settings.

---

### 1. `.python-version`

```
3.12
```

**What:** Pins the Python version for the project.
**Why:** Tools like `uv` and `pyenv` read this file to automatically use the correct Python interpreter. Ensures everyone on the team runs the same version.

---

### 2. `pyproject.toml`

**What:** The central project manifest. Declares the project name, Python version constraint, and **all dependencies** (FastAPI, SQLAlchemy, Alembic, Redis, etc.) plus dev tools (pytest, ruff, httpx).
**Why:** Replaces the old `requirements.txt` + `setup.py` combo. A single file to define deps, tool configs (ruff, pytest), and metadata. `uv sync` reads this to create a lockfile and virtual environment.

---

### 3. `uv.lock`

**What:** Auto-generated lockfile produced by `uv sync`.
**Why:** Locks exact dependency versions so every developer and CI/CD pipeline installs exactly the same packages. **Never edit manually** — it's regenerated from `pyproject.toml`.

---

### 4. `.env`

**What:** Stores real environment variables for **local development** — database credentials, Redis URL, JWT secret, etc.
**Why:** Keeps sensitive values (passwords, secret keys) out of source code. Loaded at runtime by `pydantic-settings`. **Must never be committed to git.**

---

### 5. `.env.example`

**What:** A **template** of `.env` with placeholder values and comments.
**Why:** Shows new developers exactly which variables they need to set up without exposing real secrets. Committed to git as documentation.

---

### 6. `.gitignore`

**What:** Tells Git which files/folders to ignore — `.venv/`, `.env`, `__pycache__/`, `.vscode/`, etc.
**Why:** Prevents secrets, virtual environments, and build artifacts from accidentally being committed to the repository.

---

### 7. `.dockerignore`

**What:** Tells Docker which files to exclude from the build context.
**Why:** Speeds up Docker builds and keeps the image clean by excluding `.venv/`, `.git/`, etc.

---

## Phase 2 — Core Configuration

The app needs to know how to read settings before anything else can work.

---

### 8. `app/__init__.py`

**What:** Empty file that marks the `app/` directory as a Python package.
**Why:** Required so Python can import modules like `from app.core.config import settings`.

---

### 9. `app/core/__init__.py`

**What:** Empty file marking `app/core/` as a package.
**Why:** Same as above — enables `from app.core...` imports.

---

### 10. `app/core/config.py`

**What:** Defines a `Settings` class using `pydantic-settings`. It reads all env vars from `.env` and validates them into typed Python fields: `app_name`, `debug`, `database_url`, `secret_key`, JWT params, etc.
**Why:** Centralizes all config in one place. If an env var is missing or has the wrong type, the app **crashes immediately at startup** with a clear error — no silent bugs.

---

## Phase 3 — Database Layer

Database connection and base models must exist before you can define application models.

---

### 11. `app/db/base.py`

**What:** Defines SQLAlchemy's `Base` class (the root for all ORM models) and a `TimeStampedBase` abstract model with auto-generated `id` (UUID), `created_at`, and `updated_at` columns.
**Why:** Every future model will inherit from `TimeStampedBase`, so timestamps and UUIDs are consistent across all tables automatically. DRY principle — define once, reuse everywhere.

---

### 12. `app/db/session.py`

**What:** Creates the async SQLAlchemy engine, the `AsyncSessionLocal` factory, and the Redis client — all configured from `settings`.
**Why:** These are the **actual connections** to PostgreSQL and Redis. Every database query and cache operation goes through these objects.

---

## Phase 4 — Dependencies (DI)

FastAPI uses Dependency Injection. These must be ready before writing routes.

---

### 13. `app/core/dependencies.py`

**What:** Provides `get_db()` and `get_redis()` — async generator functions that yield a DB session or Redis client.
**Why:** Used with `Depends()` in route handlers. Each request gets its own DB session that is automatically opened and closed — no manual session management, no connection leaks.

---

## Phase 5 — API Layer

With config, DB, and DI in place, we can now build routes.

---

### 14. `app/api/__init__.py`

**What:** Empty package marker for `app/api/`.
**Why:** Enables `from app.api...` imports.

---

### 15. `app/api/v1/__init__.py`

**What:** Empty package marker for `app/api/v1/`.
**Why:** The `v1` namespace allows API versioning — when you release breaking changes, you can add `v2/` without affecting `v1/`.

---

### 16. `app/api/v1/router.py`

**What:** Creates the `APIRouter` for v1. Currently empty — future feature routers (users, tasks, etc.) will be registered here.
**Why:** Central hub for all v1 endpoints. Keeps `main.py` clean by collecting all routers in one place.

---

## Phase 6 — Application Entrypoint

Everything above is assembled here.

---

### 17. `app/main.py`

**What:** The **FastAPI application factory**. It:
- Creates the `FastAPI` app instance
- Configures CORS middleware
- Registers the v1 router under `/api/v1`
- Adds a `/health` endpoint that checks DB + Redis connectivity
- Uses `lifespan` to cleanly shut down DB engine and Redis on exit

**Why:** This is the file that `uvicorn app.main:app` runs. It's the glue that wires everything together.

---

## Phase 7 — Database Migrations

Models change over time. Alembic tracks and applies schema changes.

---

### 18. `alembic.ini`

**What:** Alembic configuration file — sets the migrations folder, logging, and a placeholder DB URL (overridden at runtime).
**Why:** Alembic reads this file to know where migration scripts live and how to connect to the database.

---

### 19. `alembic/env.py`

**What:** The migration runtime. Overrides the DB URL from `settings.database_url`, imports `Base.metadata` for autogeneration, and runs migrations asynchronously.
**Why:** Bridges Alembic with our async SQLAlchemy setup. Enables `alembic revision --autogenerate` to detect model changes and `alembic upgrade head` to apply them.

---

### 20. `alembic/script.py.mako`

**What:** Mako template used by Alembic to generate new migration files.
**Why:** Provides the boilerplate for each new migration — you don't have to write it manually.

---

## Phase 8 — Placeholder Directories

Empty directories for future business logic — created now to establish the architecture pattern.

---

### 21. `app/models/` (empty)

**What:** Will contain SQLAlchemy ORM models (e.g., `User`, `Task`).
**Why:** Separates database table definitions from business logic and API routes.

---

### 22. `app/schemas/` (empty)

**What:** Will contain Pydantic schemas for request/response validation (e.g., `UserCreate`, `UserResponse`).
**Why:** Separates API data contracts from DB models. Prevents exposing internal fields (like hashed passwords).

---

### 23. `app/repository/` (empty)

**What:** Will contain repository classes — thin wrappers around DB queries.
**Why:** Isolates raw SQL/ORM queries from business logic. Makes testing easier (you can mock the repo layer).

---

### 24. `app/services/` (empty)

**What:** Will contain service classes with business logic.
**Why:** Keeps route handlers thin. Complex operations (e.g., "register a user, hash password, send email") live in services, not in route functions.

---

## Phase 9 — Testing

Tests are written alongside (or after) the code they verify.

---

### 25. `tests/__init__.py`

**What:** Empty package marker.
**Why:** Makes `tests/` importable by pytest.

---

### 26. `tests/conftest.py`

**What:** Shared pytest fixtures. Defines an async `client` fixture using `httpx.AsyncClient` + `ASGITransport` to make requests against the app **without starting a real server**.
**Why:** Every test file can inject `client` to send HTTP requests. No need for a running Uvicorn instance — tests are fast and isolated.

---

### 27. `tests/test_health.py`

**What:** Two tests for the `/health` endpoint:
1. Checks it returns HTTP 200
2. Verifies the response shape contains `status`, `version`, and `services` (database + redis)

**Why:** Smoke tests that confirm the app boots and can connect to its dependencies. These run in CI on every push.

---

## Phase 10 — Docker & Deployment

Containerization and CI/CD pipelines are typically set up last, once the app is working locally.

---

### 28. `Dockerfile`

**What:** Multi-step Docker build:
1. Starts from `python:3.12-slim`
2. Installs `uv` from the official image
3. Copies `pyproject.toml` + `uv.lock` and installs deps (cached layer)
4. Copies app code and runs Uvicorn

**Why:** Produces a lightweight, reproducible container image. Dependency layer is cached so rebuilds are fast.

---

### 29. `docker-compose.yml`

**What:** Defines 3 services:
- **api** — the FastAPI app (built from Dockerfile)
- **db** — PostgreSQL 16 with health check
- **redis** — Redis 7 with health check

API waits for DB and Redis to be healthy before starting.

**Why:** One command (`docker compose up`) spins up the entire stack locally. No manual DB/Redis installation needed.

---

### 30. `.github/workflows/ci.yml`

**What:** GitHub Actions CI pipeline triggered on every push/PR:
1. **Lint job** — runs `ruff check` and `ruff format --check`
2. **Test job** — spins up Postgres + Redis services, installs deps, runs `pytest`

**Why:** Catches code style issues and broken tests automatically before merging to main.

---

### 31. `.github/workflows/cd.yml`

**What:** GitHub Actions CD pipeline triggered on pushes to `main`:
1. **Build** — builds the Docker image and pushes it to GitHub Container Registry (GHCR)
2. **Deploy** — SSHs into the production server, pulls the new image, and restarts containers

**Why:** Automates deployment — every merge to `main` gets deployed to production without manual intervention.

---

## 📂 Final Project Structure

```
.
├── .env                          # Real secrets (git-ignored)
├── .env.example                  # Template for .env
├── .gitignore                    # Git ignore rules
├── .dockerignore                 # Docker ignore rules
├── .python-version               # Python version pin
├── pyproject.toml                # Project manifest & deps
├── uv.lock                      # Locked dependency versions
│
├── app/
│   ├── __init__.py               # Package marker
│   ├── main.py                   # FastAPI app entrypoint
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Settings from .env
│   │   └── dependencies.py       # DI: get_db(), get_redis()
│   ├── db/
│   │   ├── base.py               # Base model + TimeStampedBase
│   │   └── session.py            # Engine, session factory, Redis
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── router.py         # v1 route aggregator
│   ├── models/                   # (empty) ORM models
│   ├── schemas/                  # (empty) Pydantic schemas
│   ├── repository/               # (empty) DB query layer
│   └── services/                 # (empty) Business logic
│
├── alembic/
│   ├── env.py                    # Async migration runtime
│   ├── script.py.mako            # Migration template
│   └── versions/                 # Migration files
│
├── alembic.ini                   # Alembic config
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Shared test fixtures
│   └── test_health.py            # Health endpoint tests
│
├── Dockerfile                    # Container build
├── docker-compose.yml            # Full stack orchestration
│
└── .github/workflows/
    ├── ci.yml                    # Lint + Test pipeline
    └── cd.yml                    # Build + Deploy pipeline
```
