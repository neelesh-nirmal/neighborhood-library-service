"""Create DB tables from models. Idempotent: skips tables that already exist.

Run from apis/:  uv run python scripts/migrate.py
"""

import sys
from pathlib import Path

# Ensure apis/ is on the path so "app" resolves
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Import all models so they are registered on Base.metadata
import app.models  # noqa: F401
from app.db.base import Base
from app.db.config import get_database_url
from sqlalchemy import create_engine


def main() -> None:
    """Create all tables; no-op for existing ones."""
    url = get_database_url()
    engine = create_engine(url)
    Base.metadata.create_all(engine, checkfirst=True)
    print("Tables OK (existing ones left unchanged).")


if __name__ == "__main__":
    main()
