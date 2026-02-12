#!/bin/sh
set -e

echo "Waiting for Postgres..."
until uv run python -c "
import sys
sys.path.insert(0, '/app')
from sqlalchemy import create_engine
from app.db.config import get_database_url
engine = create_engine(get_database_url())
with engine.connect():
    pass
" 2>/dev/null; do
  echo "  Postgres not ready, retrying in 2s..."
  sleep 2
done
echo "Postgres is ready."

echo "Creating tables if not exist..."
uv run python scripts/migrate.py
echo "Seeding data if tables are empty..."
uv run python scripts/seed_data.py
echo "Starting API..."
exec "$@"
