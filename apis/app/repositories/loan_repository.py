"""Loan repository - data access for loans."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import BookCopy, Loan


class LoanRepository:
    """CRUD and queries for loans."""

    def create(
        self,
        db: Session,
        *,
        member_id: UUID,
        copy_id: UUID,
        due_at: datetime,
    ) -> Loan:
        loan = Loan(member_id=member_id, copy_id=copy_id, due_at=due_at)
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan

    def get_by_id(self, db: Session, id: UUID) -> Loan | None:
        return db.execute(select(Loan).where(Loan.id == id)).scalar_one_or_none()

    def get_active_copy_ids(self, db: Session) -> set[UUID]:
        """Copy IDs that are currently on loan (not yet returned)."""
        rows = db.execute(
            select(Loan.copy_id).where(Loan.returned_at.is_(None))
        ).scalars().all()
        # Single-column select: scalars().all() may return UUIDs or Row objects depending on driver
        return {r[0] if not isinstance(r, UUID) else r for r in rows}

    def list(
        self,
        db: Session,
        *,
        member_id: UUID | None = None,
        active_only: bool = False,
    ) -> list[Loan]:
        q = (
            select(Loan)
            .options(
                joinedload(Loan.member),
                joinedload(Loan.copy).joinedload(BookCopy.book),
            )
            .order_by(Loan.borrowed_at.desc())
        )
        if member_id is not None:
            q = q.where(Loan.member_id == member_id)
        if active_only:
            q = q.where(Loan.returned_at.is_(None))
        return list(db.execute(q).scalars().all())

    def mark_returned(self, db: Session, loan: Loan, returned_at: datetime) -> Loan:
        loan.returned_at = returned_at
        db.commit()
        db.refresh(loan)
        return loan
