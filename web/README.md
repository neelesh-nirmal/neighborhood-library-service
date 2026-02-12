# Neighborhood Library – Web (Next.js)

Minimal frontend to manage books, members, and lending. Uses **Bun** (single binary, no Node/npm required) like `uv` for Python.

## Prerequisites

- **Bun** – [Install](https://bun.sh) (one binary; no Node.js needed):

  ```bash
  curl -fsSL https://bun.sh/install | bash
  ```

  Or with Homebrew: `brew install oven-sh/bun/bun`

## Setup

```bash
cd web
bun install
cp .env.local.example .env.local   # optional; edit if API is not on localhost:8000
```

## Run

```bash
bun run dev
```

Open [http://localhost:3000](http://localhost:3000). Ensure the API is running (e.g. `cd apis && uv run main.py`) and CORS allows the frontend origin if needed.

## Scripts

| Command         | Description              |
|----------------|--------------------------|
| `bun run dev`  | Dev server (port 3000)   |
| `bun run build`| Production build        |
| `bun run start`| Serve production build  |
| `bun run lint` | Run Next.js lint        |

## Use case flow

1. **Books** – Add catalog entries (title, author, optional ISBN/description).
2. **Members** – Add members (name, optional email/phone).
3. **Copies** – For a book, add physical copies (copy code / barcode).
4. **Borrow / Return** – Select member and copy, set due date, click Borrow. Return from the Loans tab.
5. **Loans** – List all loans; filter by member (e.g. “books this member has out”) and/or “Active only”.
