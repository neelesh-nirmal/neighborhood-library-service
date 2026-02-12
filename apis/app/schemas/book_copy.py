"""Book copy request/response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BookCopyCreate(BaseModel):
    """Payload to create a book copy."""

    copy_code: str = Field(..., min_length=1, max_length=64)


class BookCopyResponse(BaseModel):
    """Book copy in API responses."""

    id: UUID
    book_id: UUID
    copy_code: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
