"""Book repository - data access for books."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Book


class BookRepository:
    """CRUD and queries for books."""

    def create(self, db: Session, *, title: str, author: str, description: str | None = None, isbn: str | None = None) -> Book:
        book = Book(title=title, author=author, description=description, isbn=isbn)
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    def get_by_id(self, db: Session, id: UUID) -> Book | None:
        return db.execute(select(Book).where(Book.id == id)).scalar_one_or_none()

    def list_all(self, db: Session) -> list[Book]:
        return list(db.execute(select(Book).order_by(Book.title)).scalars().all())

    def update(
        self,
        db: Session,
        book: Book,
        *,
        title: str | None = None,
        author: str | None = None,
        description: str | None = None,
        isbn: str | None = None,
    ) -> Book:
        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if description is not None:
            book.description = description
        if isbn is not None:
            book.isbn = isbn
        db.commit()
        db.refresh(book)
        return book
