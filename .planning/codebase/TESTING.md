# TESTING.md
<!-- last_mapped: 2026-05-10 -->

## Current State

**No tests implemented.** The `test/` directory exists but is empty.

## Test Infrastructure

- No test framework configured in `pyproject.toml` (no pytest, unittest, etc.)
- No test dependencies declared
- No CI pipeline configured (`.github/workflows/ci.yml` is empty)
- No coverage tooling present

## Expected Test Stack (FastAPI convention)

When tests are added, the standard FastAPI stack would be:

| Tool | Purpose |
|------|---------|
| `pytest` | Test runner |
| `pytest-asyncio` | Async test support |
| `httpx` + `AsyncClient` | FastAPI test client |
| `pytest-postgresql` or test containers | Isolated DB per test |

## Test Location

- `test/` — root-level test directory (currently empty)

## Patterns to Adopt

- Use `AsyncClient` from `httpx` with FastAPI's `ASGITransport`
- Override `get_db` dependency for test isolation
- Use `TimeStampedBase.metadata.create_all()` against a test DB
- Scope DB fixtures at `session` or `function` level depending on isolation needs
