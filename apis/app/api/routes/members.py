"""Member controllers - HTTP layer."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.member import MemberCreate, MemberResponse, MemberUpdate
from app.services import MemberService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/members", tags=["members"])


def get_member_service(db: Session = Depends(get_db)) -> MemberService:
    return MemberService(db)


@router.post("", response_model=MemberResponse, status_code=201)
def create_member(
    body: MemberCreate,
    service: MemberService = Depends(get_member_service),
) -> MemberResponse:
    """Create a new member."""
    member = service.create_member(
        name=body.name,
        email=body.email,
        phone=body.phone,
    )
    return MemberResponse.model_validate(member)


@router.get("", response_model=list[MemberResponse])
def list_members(service: MemberService = Depends(get_member_service)) -> list[MemberResponse]:
    """List all members."""
    members = service.list_members()
    return [MemberResponse.model_validate(m) for m in members]


@router.get("/{member_id}", response_model=MemberResponse)
def get_member(
    member_id: UUID,
    service: MemberService = Depends(get_member_service),
) -> MemberResponse:
    """Get a member by ID."""
    member = service.get_member(member_id)
    if member is None:
        logger.warning("Get member failed: member_id=%s not found", member_id)
        raise HTTPException(status_code=404, detail="Member not found")
    return MemberResponse.model_validate(member)


@router.put("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: UUID,
    body: MemberUpdate,
    service: MemberService = Depends(get_member_service),
) -> MemberResponse:
    """Update a member (partial)."""
    member = service.update_member(
        member_id,
        name=body.name,
        email=body.email,
        phone=body.phone,
    )
    if member is None:
        logger.warning("Update member failed: member_id=%s not found", member_id)
        raise HTTPException(status_code=404, detail="Member not found")
    return MemberResponse.model_validate(member)
