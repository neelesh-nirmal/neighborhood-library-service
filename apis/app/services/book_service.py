"""Book service - business logic for books and copies."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Book, BookCopy
from app.repositories import BookCopyRepository, BookRepository


class BookService:
    """Orchestrates book and copy operations."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._book_repo = BookRepository()
        self._copy_repo = BookCopyRepository()

    def create_book(
        self,
        *,
        title: str,
        author: str,
        description: str | None = None,
        isbn: str | None = None,
    ) -> Book:
        return self._book_repo.create(
            self._db,
            title=title,
            author=author,
            description=description,
            isbn=isbn,
        )

    def get_book(self, book_id: UUID) -> Book | None:
        return self._book_repo.get_by_id(self._db, book_id)

    def list_books(self) -> list[Book]:
        return self._book_repo.list_all(self._db)

    def update_book(
        self,
        book_id: UUID,
        *,
        title: str | None = None,
        author: str | None = None,
        description: str | None = None,
        isbn: str | None = None,
    ) -> Book | None:
        book = self._book_repo.get_by_id(self._db, book_id)
        if book is None:
            return None
        return self._book_repo.update(
            self._db,
            book,
            title=title,
            author=author,
            description=description,
            isbn=isbn,
        )

    def create_copy(self, book_id: UUID, *, copy_code: str) -> BookCopy | None:
        book = self._book_repo.get_by_id(self._db, book_id)
        if book is None:
            return None
        return self._copy_repo.create(self._db, book_id=book_id, copy_code=copy_code)

    def get_copy(self, copy_id: UUID) -> BookCopy | None:
        return self._copy_repo.get_by_id(self._db, copy_id)

    def list_copies_for_book(self, book_id: UUID) -> list[BookCopy]:
        return self._copy_repo.list_by_book_id(self._db, book_id)
