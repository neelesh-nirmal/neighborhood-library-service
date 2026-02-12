# Deploy

Run the full stack (PostgreSQL, API, Web) with Docker Compose.

## Quick start

From this directory:

```bash
docker compose up -d --build
```

- **Web UI:** http://localhost:3000  
- **API:** http://localhost:8000 (docs: http://localhost:8000/docs)  
- **PostgreSQL:** localhost:5432 (see below)

The API runs migrations on startup. To seed books, members, and copies, run once:

```bash
docker compose exec api uv run python scripts/seed_data.py
```

## Services

| Service   | Port | Description                    |
|----------|------|--------------------------------|
| postgres | 5432 | Database                       |
| api      | 8000 | FastAPI (migrates on startup)  |
| web      | 3000 | Next.js frontend               |

## PostgreSQL (direct connection)

| Setting   | Value                |
|----------|----------------------|
| Host     | `localhost`          |
| Port     | `5432`               |
| User     | `postgres`           |
| Password | `postgres`           |
| Database | `neighborhood_library` |

**Connection string:**  
`postgresql://postgres:postgres@localhost:5432/neighborhood_library`

## Commands

```bash
# Start (build if needed)
docker compose up -d --build

# View logs
docker compose logs -f

# Stop
docker compose down

# Stop and remove volumes (wipe DB)
docker compose down -v
```

Data is stored in the `postgres_data` volume.
