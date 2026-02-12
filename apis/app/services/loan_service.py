"""Loan service - business logic for borrowing and returning."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Loan
from app.repositories import BookCopyRepository, LoanRepository, MemberRepository


class LoanService:
    """Orchestrates borrow/return and loan queries."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._loan_repo = LoanRepository()
        self._member_repo = MemberRepository()
        self._copy_repo = BookCopyRepository()

    def borrow(
        self,
        *,
        member_id: UUID,
        copy_id: UUID,
        due_at: datetime,
    ) -> tuple[Loan | None, str | None]:
        """Create a loan. Returns (loan, None) or (None, error_message)."""
        member = self._member_repo.get_by_id(self._db, member_id)
        if member is None:
            return None, "Member not found"
        copy = self._copy_repo.get_by_id(self._db, copy_id)
        if copy is None:
            return None, "Book copy not found"
        try:
            loan = self._loan_repo.create(
                self._db,
                member_id=member_id,
                copy_id=copy_id,
                due_at=due_at,
            )
            return loan, None
        except Exception as e:
            self._db.rollback()
            if "ix_loans_active_copy" in str(e) or "unique" in str(e).lower():
                return None, "Copy is already on loan"
            return None, str(e)

    def borrow_by_book(
        self,
        *,
        member_id: UUID,
        book_id: UUID,
        due_at: datetime,
    ) -> tuple[Loan | None, str | None]:
        """Create a loan by picking any available copy of the book. Returns (loan, None) or (None, error_message)."""
        member = self._member_repo.get_by_id(self._db, member_id)
        if member is None:
            return None, "Member not found"
        copies = self._copy_repo.list_by_book_id(self._db, book_id)
        if not copies:
            return None, "Book has no copies"
        on_loan = self._loan_repo.get_active_copy_ids(self._db)
        for copy in copies:
            if copy.id not in on_loan:
                return self.borrow(member_id=member_id, copy_id=copy.id, due_at=due_at)
        return None, "No available copy for this book (all copies are on loan)"

    def return_loan(self, loan_id: UUID) -> tuple[Loan | None, str | None]:
        """Mark loan as returned. Returns (loan, None) or (None, error_message)."""
        loan = self._loan_repo.get_by_id(self._db, loan_id)
        if loan is None:
            return None, "Loan not found"
        if loan.returned_at is not None:
            return None, "Loan already returned"
        now = datetime.now(timezone.utc)
        return self._loan_repo.mark_returned(self._db, loan, now), None

    def get_loan(self, loan_id: UUID) -> Loan | None:
        return self._loan_repo.get_by_id(self._db, loan_id)

    def list_loans(
        self,
        *,
        member_id: UUID | None = None,
        active_only: bool = False,
    ) -> list[Loan]:
        return self._loan_repo.list(self._db, member_id=member_id, active_only=active_only)
