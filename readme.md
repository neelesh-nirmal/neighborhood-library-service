# Neighborhood Library Service

## Deploy

```bash
cd deploy
docker compose up -d --build
```

Startup: API waits for Postgres, creates tables if missing, seeds when empty, then serves.

## Where to access

| What | URL |
|------|-----|
| Web UI | http://localhost:3000 |
| API docs (Swagger) | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health | http://localhost:8000/api/v1/health |

## Compose commands

```bash
docker compose up -d --build   # start
docker compose logs -f        # logs
docker compose down            # stop
docker compose down -v         # stop and remove DB volume
```

## Postgres (direct)

- Host: `localhost`, Port: `5432`, User: `postgres`, Password: `postgres`, DB: `neighborhood_library`
- URL: `postgresql://postgres:postgres@localhost:5432/neighborhood_library`
