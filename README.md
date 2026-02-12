# Neighborhood Library Service

Library app for books, members, and lending. Stack: FastAPI, PostgreSQL, Next.js.

---

## Quick start

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) and Docker Compose.

```bash
cd deploy
docker compose up -d --build
```

Tables are created and seed data loaded on first run. No extra steps.

- **Web UI:** http://localhost:3000  
- **API docs:** http://localhost:8000/docs  

---

## Screenshots

| Description | Screenshot |
|-------------|------------|
| Books (catalog) | ![Books](docs/screenshots/books.png) |
| Members | ![Members](docs/screenshots/members.png) |
| Book copies | ![Copies](docs/screenshots/copies.png) |
| Borrow a book | ![Borrow & return](docs/screenshots/borrow-return.png) |
| Loans | ![Loans](docs/screenshots/loans.png) |

---

## Endpoints

| Resource   | URL |
|-----------|-----|
| Web UI    | http://localhost:3000 |
| API docs  | http://localhost:8000/docs |
| ReDoc     | http://localhost:8000/redoc |

**API base:** `http://localhost:8000/api/v1`

| Method | Path | Description |
|--------|------|-------------|
| GET    | /health | Health check |
| GET    | /books | List books |
| POST   | /books | Create book |
| GET    | /books/{book_id} | Get book |
| PUT    | /books/{book_id} | Update book |
| GET    | /books/{book_id}/copies | List copies for book |
| POST   | /books/{book_id}/copies | Add copy |
| GET    | /members | List members |
| POST   | /members | Create member |
| GET    | /members/{member_id} | Get member |
| PUT    | /members/{member_id} | Update member |
| GET    | /loans | List loans (query: `member_id`, `active_only`) |
| POST   | /loans | Borrow by copy (body: member_id, copy_id, due_at) |
| POST   | /loans/by-book | Borrow by book — auto-assigns an available copy (body: member_id, book_id, due_at) |
| GET    | /loans/{loan_id} | Get loan |
| POST   | /loans/{loan_id}/return | Return book |

---

## Docker

| Action   | Command |
|----------|---------|
| Start    | `docker compose up -d --build` |
| Logs     | `docker compose logs -f` |
| Stop     | `docker compose down` |
| Reset DB | `docker compose down -v` |

---

## Database

| Field    | Value |
|----------|--------|
| Host     | localhost |
| Port     | 5432 |
| User     | postgres |
| Password | postgres |
| Database | neighborhood_library |

Connection string: `postgresql://postgres:postgres@localhost:5432/neighborhood_library`

**Clean / reset database**

| Context | Command |
|---------|---------|
| Docker (remove DB volume, then start again to get fresh DB + seed) | `cd deploy && docker compose down -v` then `docker compose up -d --build` |
| Local dev (drop tables, recreate; run from `apis/`) | `uv run python scripts/migrate.py --clean` |

---

## Architecture

### DB schema

```mermaid
erDiagram
  Book ||--o{ BookCopy : has
  BookCopy ||--o{ Loan : lent via
  Member ||--o{ Loan : borrows
  Book {
    uuid id PK
    string title
    string author
    string isbn
    text description
    timestamptz created_at
    timestamptz updated_at
  }
  BookCopy {
    uuid id PK
    uuid book_id FK
    string copy_code UK
    timestamptz created_at
    timestamptz updated_at
  }
  Member {
    uuid id PK
    string name
    string email UK
    string phone
    timestamptz created_at
    timestamptz updated_at
  }
  Loan {
    uuid id PK
    uuid member_id FK
    uuid copy_id FK
    timestamptz borrowed_at
    timestamptz due_at
    timestamptz returned_at
    timestamptz created_at
    timestamptz updated_at
  }
```

- One active loan per copy: unique partial index on `loans.copy_id` where `returned_at IS NULL`. FKs use `ON DELETE RESTRICT`.

### Project structure

```
neighborhood-library-service/
├── apis/
│   ├── app/
│   │   ├── api/routes/      # HTTP handlers (controllers)
│   │   ├── services/        # Business logic
│   │   ├── repositories/   # Data access
│   │   ├── schemas/        # Pydantic request/response
│   │   ├── models/         # SQLAlchemy ORM
│   │   └── db/             # Session, config, base
│   ├── scripts/
│   │   ├── migrate.py      # Create tables; --clean to drop+create
│   │   ├── seed_data.py    # Seed books, members, copies
│   │   └── entrypoint.sh   # Wait Postgres → migrate → seed → uvicorn
│   └── main.py
├── web/
│   ├── app/                # App Router (layout, page)
│   ├── components/         # UI sections (Books, Members, Copies, Borrow, Loans)
│   └── lib/
│       └── api.ts          # API client and types
└── deploy/
    └── docker-compose.yml  # postgres, api, web
```

### Request flow

```mermaid
flowchart LR
  subgraph client [Browser]
    UI[Web UI]
  end
  subgraph web [Next.js :3000]
    APIClient[API client]
  end
  subgraph api [FastAPI :8000]
    Routes[routes]
    Services[services]
    Repos[repositories]
  end
  subgraph db [PostgreSQL :5432]
    PG[(DB)]
  end
  UI -->|NEXT_PUBLIC_API_URL| APIClient
  APIClient -->|HTTP| Routes
  Routes --> Services
  Services --> Repos
  Repos --> PG
```

---

## Developer setup

**Prerequisites:** PostgreSQL, [uv](https://docs.astral.sh/uv/) (Python), [Bun](https://bun.sh) (JS).

**API (apis/):**

```bash
cd apis
uv sync
uv run python scripts/migrate.py
uv run python scripts/seed_data.py
uv run python main.py
```

- Reset DB: `uv run python scripts/migrate.py --clean`
- `DATABASE_URL` default: `postgresql://postgres:postgres@localhost:5432/neighborhood_library`

**Web (web/):**

```bash
cd web
bun install
bun run dev
```

Optional: `cp .env.local.example .env.local`, set `NEXT_PUBLIC_API_URL` (default `http://localhost:8000/api/v1`). Scripts: `bun run dev` | `bun run build` | `bun run start` | `bun run lint`.

**Local run order:** 
1. Postgres (`cd deploy && docker compose up -d postgres`). 
2. API in `apis/`. 
3. Web in `web/` → http://localhost:3000.
