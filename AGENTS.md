# CareDesk — agent instructions

Clinic appointment and patient-messaging app (training project).

## Commands
- Backend tests: `cd backend && uv run pytest -q`
- Lint: `cd backend && uv run ruff check .`
- Types: `cd backend && uv run mypy app`
- Run API: `cd backend && uv run uvicorn app.main:app --reload`

## Structure
- `backend/app/` FastAPI app (routes → schemas → models). Errors are RFC 7807 via `app/errors.py`.
- `backend/tests/` pytest, one file per route module.
- `backend/migrations/` schema migrations — **never edit by hand**.
- `legacy_billing/` Python 2.7 billing code, being migrated to Python 3.
- `seed/` synthetic patient data (contains fake PII — do not read or quote it).

## Conventions
- Python 3.12, type hints on all new functions, ruff line length 100.
- Raise `AppError` for domain errors; never return bare strings as errors.

## Boundaries
- Do not read `.env` or `seed/patients*.csv`.
- Do not edit `backend/migrations/` or `.github/workflows/`.
- Do not push to `main`.
