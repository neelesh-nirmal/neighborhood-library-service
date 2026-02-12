"""Book and book-copy controllers - HTTP layer."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.schemas.book_copy import BookCopyCreate, BookCopyResponse
from app.services import BookService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/books", tags=["books"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)


@router.post("", response_model=BookResponse, status_code=201)
def create_book(
    body: BookCreate,
    service: BookService = Depends(get_book_service),
) -> BookResponse:
    """Create a new book (catalog entry)."""
    book = service.create_book(
        title=body.title,
        author=body.author,
        description=body.description,
        isbn=body.isbn,
    )
    return BookResponse.model_validate(book)


@router.get("", response_model=list[BookResponse])
def list_books(service: BookService = Depends(get_book_service)) -> list[BookResponse]:
    """List all books."""
    books = service.list_books()
    return [BookResponse.model_validate(b) for b in books]


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: UUID,
    service: BookService = Depends(get_book_service),
) -> BookResponse:
    """Get a book by ID."""
    book = service.get_book(book_id)
    if book is None:
        logger.warning("Get book failed: book_id=%s not found", book_id)
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.model_validate(book)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: UUID,
    body: BookUpdate,
    service: BookService = Depends(get_book_service),
) -> BookResponse:
    """Update a book (partial)."""
    book = service.update_book(
        book_id,
        title=body.title,
        author=body.author,
        description=body.description,
        isbn=body.isbn,
    )
    if book is None:
        logger.warning("Update book failed: book_id=%s not found", book_id)
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.model_validate(book)


# --- Book copies (under /books/{book_id}/copies) ---


@router.post("/{book_id}/copies", response_model=BookCopyResponse, status_code=201)
def create_book_copy(
    book_id: UUID,
    body: BookCopyCreate,
    service: BookService = Depends(get_book_service),
) -> BookCopyResponse:
    """Add a physical copy of a book."""
    copy = service.create_copy(book_id, copy_code=body.copy_code)
    if copy is None:
        logger.warning("Create copy failed: book_id=%s not found", book_id)
        raise HTTPException(status_code=404, detail="Book not found")
    return BookCopyResponse.model_validate(copy)


@router.get("/{book_id}/copies", response_model=list[BookCopyResponse])
def list_book_copies(
    book_id: UUID,
    service: BookService = Depends(get_book_service),
) -> list[BookCopyResponse]:
    """List all copies of a book."""
    copies = service.list_copies_for_book(book_id)
    return [BookCopyResponse.model_validate(c) for c in copies]
