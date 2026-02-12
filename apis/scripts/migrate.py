"""Create DB tables from models. Idempotent: skips tables that already exist.

Run from apis/:
  uv run python scripts/migrate.py           # create missing tables only
  uv run python scripts/migrate.py --clean   # drop all tables, then create
"""

import argparse
import logging
import sys
from pathlib import Path

# Ensure apis/ is on the path so "app" resolves
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Import all models so they are registered on Base.metadata (path set above)
import app.models  # noqa: F401, E402
from app.db.base import Base  # noqa: E402
from app.db.config import get_database_url  # noqa: E402
from sqlalchemy import create_engine


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or reset DB tables.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Drop all tables then create them (clean slate).",
    )
    args = parser.parse_args()

    try:
        url = get_database_url()
        engine = create_engine(url)

        if args.clean:
            Base.metadata.drop_all(engine, checkfirst=True)
            logger.info("Dropped all tables.")

        Base.metadata.create_all(engine, checkfirst=True)
        logger.info("Tables OK.")
    except Exception as e:
        logger.exception("Migration failed: %s", e)
        raise


if __name__ == "__main__":
    main()
