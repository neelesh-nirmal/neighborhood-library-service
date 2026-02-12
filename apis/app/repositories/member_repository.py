"""Member repository - data access for members."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Member


class MemberRepository:
    """CRUD and queries for members."""

    def create(
        self,
        db: Session,
        *,
        name: str,
        email: str | None = None,
        phone: str | None = None,
    ) -> Member:
        member = Member(name=name, email=email, phone=phone)
        db.add(member)
        db.commit()
        db.refresh(member)
        return member

    def get_by_id(self, db: Session, id: UUID) -> Member | None:
        return db.execute(select(Member).where(Member.id == id)).scalar_one_or_none()

    def list_all(self, db: Session) -> list[Member]:
        return list(db.execute(select(Member).order_by(Member.name)).scalars().all())

    def update(
        self,
        db: Session,
        member: Member,
        *,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> Member:
        if name is not None:
            member.name = name
        if email is not None:
            member.email = email
        if phone is not None:
            member.phone = phone
        db.commit()
        db.refresh(member)
        return member
