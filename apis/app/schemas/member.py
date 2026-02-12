"""Member request/response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MemberCreate(BaseModel):
    """Payload to create a member."""

    name: str = Field(..., min_length=1, max_length=255)
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=50)


class MemberUpdate(BaseModel):
    """Payload to update a member (partial)."""

    name: str | None = Field(None, min_length=1, max_length=255)
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=50)


class MemberResponse(BaseModel):
    """Member in API responses."""

    id: UUID
    name: str
    email: str | None
    phone: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
