# Neighborhood Library Service API

FastAPI service with a health check endpoint.

## Setup

```bash
uv sync
```

## Run

```bash
uv run python main.py
```

Server runs at `http://0.0.0.0:8000`.

- **Health:** `GET /api/v1/health`
- **Docs:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Database

Models live in `app/models/`. Create tables (idempotent—run anytime, skips existing tables):

```bash
# Ensure Postgres is running (e.g. deploy/docker-compose up -d)
uv run python scripts/migrate.py
```

Add or change models in `app/models/`, then run the same command again. Set `DATABASE_URL` if needed (default: `postgresql://postgres:postgres@localhost:5432/neighborhood_library`).

## Type check

```bash
uv run mypy app main.py
```
