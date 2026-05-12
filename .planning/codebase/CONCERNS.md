# CONCERNS.md
<!-- last_mapped: 2026-05-10 -->

## Project Maturity

This is an early-stage scaffold. Most application layers are empty directories. The concerns below are about what needs to be built, not defects in existing code.

---

## High Priority

### No database migrations
- **Risk**: Schema changes will require manual SQL or `metadata.create_all()` drops
- **Fix**: Add `alembic` — standard SQLAlchemy migration tool. Initialize with `alembic init` and wire to `Base.metadata`
- **Files**: `app/db/base.py` (`Base` imported by alembic `env.py`)

### No authentication implementation
- **Risk**: JWT settings are configured but no auth logic exists. Anyone can call any future endpoint.
- **Fix**: Implement auth routes (`/auth/login`, `/auth/refresh`) + `get_current_user` dependency before adding protected endpoints
- **Files**: `app/core/dependencies.py` (add dependency), `app/api/` (add routes)

### No tests
- **Risk**: No regression coverage as features are added. Empty CI pipeline gives false confidence.
- **Fix**: Add pytest + pytest-asyncio, write at minimum health check test and auth flow test
- **Files**: `test/`, `.github/workflows/ci.yml`

### Empty CI/CD pipelines
- **Risk**: `.github/workflows/ci.yml` and `cd.yml` are present but completely empty — no linting, testing, or deployment
- **Fix**: Add basic CI: install deps, run tests, type-check

---

## Medium Priority

### Redis not integrated
- **Risk**: Redis is in `docker-compose.yml` but no client in the app. If it's needed for caching/rate-limiting/sessions, it's dead infrastructure today.
- **Fix**: Add `redis-py` or `aioredis` dependency and integration, or remove from docker-compose if not needed

### No linting or formatting config
- **Risk**: Without `ruff` or `black` config, code style will drift as the project grows
- **Fix**: Add `ruff` to dev dependencies, configure in `pyproject.toml`

### Project name mismatch
- **Risk**: `pyproject.toml` has `name = "test"` but `.env.example` shows `APP_NAME=claude code clone`. Misleading.
- **Fix**: Rename `pyproject.toml` project name to match actual project

### `main.py` root stub disconnected
- **Risk**: `main.py` at root prints "Hello from test!" and is unrelated to the FastAPI app. Confusing for new contributors.
- **Fix**: Either delete it or repurpose as a CLI entry point

---

## Low Priority

### `ALLOWED_ORIGINS` default in `.env.example`
- **Risk**: `ALLOWED_ORIGINS=[""]` — the default is an empty string inside a list, not an empty list. This could cause unexpected CORS behavior.
- **Fix**: Change to `ALLOWED_ORIGINS=["http://localhost:3000"]` or `ALLOWED_ORIGINS=[]`

### No `__init__.py` in `api/`, `models/`, `repository/`, `schemas/`, `services/`
- **Risk**: Empty directories have no `__init__.py`. Python will still treat them as packages via implicit namespace packages (Python 3.3+), but explicit `__init__.py` is cleaner.
- **Fix**: Add empty `__init__.py` to each when files are added

### README is empty
- **Risk**: `README.md` is empty — no setup instructions, no architecture overview
- **Fix**: Add basic setup and run instructions
