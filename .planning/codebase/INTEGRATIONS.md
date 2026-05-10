# INTEGRATIONS.md
<!-- last_mapped: 2026-05-10 -->

## Database

- **PostgreSQL 16** via asyncpg
- Connection configured in `app/db/session.py` using `DATABASE_URL` env var
- Docker service name: `db` (host override in docker-compose env)
- Local: `postgresql+asyncpg://postgres:yourpassword@localhost:5432/todo_db`
- Docker: `postgresql+asyncpg://postgres:postgres@db:5432/todo_db`

## Cache / Broker

- **Redis 7** — defined in `docker-compose.yml`, health-checked
- Port: 6379 (exposed to host)
- **Not yet integrated** into app code — no redis client imported

## Auth

- **JWT-based authentication** — configured but not yet implemented
- Settings present: `SECRET_KEY`, `ALGORITHM` (HS256), `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
- No auth library imported yet (likely will use `python-jose` or `PyJWT`)

## CI/CD

- **GitHub Actions** — two workflow files present but empty:
  - `.github/workflows/ci.yml`
  - `.github/workflows/cd.yml`

## External APIs

None integrated yet.

## Webhooks

None implemented.
