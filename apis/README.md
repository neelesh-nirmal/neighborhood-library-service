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

## Type check

```bash
uv run mypy app main.py
```
