"""Loan request/response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class LoanCreate(BaseModel):
    """Payload to borrow a book (create a loan)."""

    member_id: UUID
    copy_id: UUID
    due_at: datetime = Field(..., description="When the book must be returned")


class LoanResponse(BaseModel):
    """Loan in API responses."""

    id: UUID
    member_id: UUID
    copy_id: UUID
    borrowed_at: datetime
    due_at: datetime
    returned_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LoanWithDetailsResponse(BaseModel):
    """Loan with member and copy (book) details for listing."""

    id: UUID
    member_id: UUID
    member_name: str
    copy_id: UUID
    copy_code: str
    book_id: UUID
    book_title: str
    book_author: str
    borrowed_at: datetime
    due_at: datetime
    returned_at: datetime | None

    model_config = {"from_attributes": True}
