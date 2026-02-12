"""Book request/response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    """Payload to create a book."""

    title: str = Field(..., min_length=1, max_length=512)
    author: str = Field(..., min_length=1, max_length=512)
    description: str | None = Field(None, max_length=10_000)
    isbn: str | None = Field(None, max_length=20)


class BookUpdate(BaseModel):
    """Payload to update a book (partial)."""

    title: str | None = Field(None, min_length=1, max_length=512)
    author: str | None = Field(None, min_length=1, max_length=512)
    description: str | None = None
    isbn: str | None = Field(None, max_length=20)


class BookResponse(BaseModel):
    """Book in API responses."""

    id: UUID
    title: str
    author: str
    description: str | None
    isbn: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
