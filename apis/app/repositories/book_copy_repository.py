"""Book copy repository - data access for book copies."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import BookCopy


class BookCopyRepository:
    """CRUD and queries for book copies."""

    def create(self, db: Session, *, book_id: UUID, copy_code: str) -> BookCopy:
        copy = BookCopy(book_id=book_id, copy_code=copy_code)
        db.add(copy)
        db.commit()
        db.refresh(copy)
        return copy

    def get_by_id(self, db: Session, id: UUID) -> BookCopy | None:
        return db.execute(select(BookCopy).where(BookCopy.id == id)).scalar_one_or_none()

    def list_by_book_id(self, db: Session, book_id: UUID) -> list[BookCopy]:
        return list(
            db.execute(select(BookCopy).where(BookCopy.book_id == book_id).order_by(BookCopy.copy_code)).scalars().all()
        )

    def get_by_copy_code(self, db: Session, copy_code: str) -> BookCopy | None:
        return db.execute(select(BookCopy).where(BookCopy.copy_code == copy_code)).scalar_one_or_none()
