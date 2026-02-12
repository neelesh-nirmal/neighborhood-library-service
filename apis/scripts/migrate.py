"""Create DB tables from models. Idempotent: skips tables that already exist.

Run from apis/:
  uv run python scripts/migrate.py           # create missing tables only
  uv run python scripts/migrate.py --clean   # drop all tables, then create
"""

import argparse
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
    parser = argparse.ArgumentParser(description="Create or reset DB tables.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Drop all tables then create them (clean slate).",
    )
    args = parser.parse_args()

    url = get_database_url()
    engine = create_engine(url)

    if args.clean:
        Base.metadata.drop_all(engine, checkfirst=True)
        print("Dropped all tables.")

    Base.metadata.create_all(engine, checkfirst=True)
    print("Tables OK.")


if __name__ == "__main__":
    main()
