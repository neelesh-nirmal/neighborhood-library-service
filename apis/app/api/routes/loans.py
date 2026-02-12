"""Loan controllers - borrow/return and list."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.loan import LoanCreate, LoanCreateByBook, LoanResponse, LoanWithDetailsResponse
from app.services import LoanService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/loans", tags=["loans"])


def get_loan_service(db: Session = Depends(get_db)) -> LoanService:
    return LoanService(db)


@router.post("", response_model=LoanResponse, status_code=201)
def borrow_book(
    body: LoanCreate,
    service: LoanService = Depends(get_loan_service),
) -> LoanResponse:
    """Record that a member is borrowing a book copy."""
    loan, err = service.borrow(
        member_id=body.member_id,
        copy_id=body.copy_id,
        due_at=body.due_at,
    )
    if err is not None:
        if "not found" in err.lower():
            logger.warning("Borrow failed (not found): %s", err)
            raise HTTPException(status_code=404, detail=err)
        logger.warning("Borrow failed: %s", err)
        raise HTTPException(status_code=400, detail=err)
    return LoanResponse.model_validate(loan)


@router.post("/by-book", response_model=LoanResponse, status_code=201)
def borrow_book_by_book(
    body: LoanCreateByBook,
    service: LoanService = Depends(get_loan_service),
) -> LoanResponse:
    """Borrow any available copy of a book. A copy is assigned automatically."""
    loan, err = service.borrow_by_book(
        member_id=body.member_id,
        book_id=body.book_id,
        due_at=body.due_at,
    )
    if err is not None:
        if "not found" in err.lower():
            logger.warning("Borrow by book failed (not found): %s", err)
            raise HTTPException(status_code=404, detail=err)
        logger.warning("Borrow by book failed: %s", err)
        raise HTTPException(status_code=400, detail=err)
    return LoanResponse.model_validate(loan)


@router.post("/{loan_id}/return", response_model=LoanResponse)
def return_book(
    loan_id: UUID,
    service: LoanService = Depends(get_loan_service),
) -> LoanResponse:
    """Record that a borrowed book has been returned."""
    loan, err = service.return_loan(loan_id)
    if err is not None:
        if "not found" in err.lower():
            logger.warning("Return failed (not found): %s", err)
            raise HTTPException(status_code=404, detail=err)
        logger.warning("Return failed: %s", err)
        raise HTTPException(status_code=400, detail=err)
    return LoanResponse.model_validate(loan)


@router.get("", response_model=list[LoanWithDetailsResponse])
def list_loans(
    member_id: UUID | None = Query(None, description="Filter by member (e.g. books a member has out)"),
    active_only: bool = Query(False, description="Only loans not yet returned"),
    service: LoanService = Depends(get_loan_service),
) -> list[LoanWithDetailsResponse]:
    """List loans; optionally filter by member and/or active only."""
    loans = service.list_loans(member_id=member_id, active_only=active_only)
    result: list[LoanWithDetailsResponse] = []
    for loan in loans:
        result.append(
            LoanWithDetailsResponse(
                id=loan.id,
                member_id=loan.member_id,
                member_name=loan.member.name,
                copy_id=loan.copy_id,
                copy_code=loan.copy.copy_code,
                book_id=loan.copy.book_id,
                book_title=loan.copy.book.title,
                book_author=loan.copy.book.author,
                borrowed_at=loan.borrowed_at,
                due_at=loan.due_at,
                returned_at=loan.returned_at,
            )
        )
    return result


@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(
    loan_id: UUID,
    service: LoanService = Depends(get_loan_service),
) -> LoanResponse:
    """Get a loan by ID."""
    loan = service.get_loan(loan_id)
    if loan is None:
        logger.warning("Get loan failed: loan_id=%s not found", loan_id)
        raise HTTPException(status_code=404, detail="Loan not found")
    return LoanResponse.model_validate(loan)
