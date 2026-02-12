# Developer setup

## Prerequisites

- **PostgreSQL** (or run only DB: `cd deploy && docker compose up -d postgres`)
- **uv** (Python): https://docs.astral.sh/uv/
- **Bun** (JS/Next): https://bun.sh or `brew install oven-sh/bun/bun`

## API (apis/)

```bash
cd apis
uv sync
```

Create tables and seed (Postgres must be running):

```bash
uv run python scripts/migrate.py
uv run python scripts/seed_data.py
```

Run API:

```bash
uv run python main.py
```

- Reset DB: `uv run python scripts/migrate.py --clean`
- `DATABASE_URL` default: `postgresql://postgres:postgres@localhost:5432/neighborhood_library`

## Web (web/)

```bash
cd web
bun install
```

Optional: `cp .env.local.example .env.local` and set `NEXT_PUBLIC_API_URL` (default `http://localhost:8000/api/v1`).

```bash
bun run dev
```

- Dev: `bun run dev` (port 3000)
- Build: `bun run build`
- Start (prod): `bun run start`
- Lint: `bun run lint`

## Order for local run

1. Start Postgres (`deploy/docker compose up -d postgres`).
2. In `apis/`: migrate, seed, then `uv run python main.py`.
3. In `web/`: `bun run dev`. Open http://localhost:3000.
