"""Database session - engine, session factory, and FastAPI dependency."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.db.config import get_database_url

engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,
    echo=False,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """Yield a DB session for the request; closed when request ends."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
