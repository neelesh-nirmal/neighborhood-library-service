"""Database configuration - URL from environment."""

import os


def get_database_url() -> str:
    """Return the database URL, defaulting to local Postgres from deploy compose."""
    return os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/neighborhood_library",
    )
