"""Member service - business logic for members."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Member
from app.repositories import MemberRepository


class MemberService:
    """Orchestrates member operations."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._repo = MemberRepository()

    def create_member(
        self,
        *,
        name: str,
        email: str | None = None,
        phone: str | None = None,
    ) -> Member:
        return self._repo.create(self._db, name=name, email=email, phone=phone)

    def get_member(self, member_id: UUID) -> Member | None:
        return self._repo.get_by_id(self._db, member_id)

    def list_members(self) -> list[Member]:
        return self._repo.list_all(self._db)

    def update_member(
        self,
        member_id: UUID,
        *,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> Member | None:
        member = self._repo.get_by_id(self._db, member_id)
        if member is None:
            return None
        return self._repo.update(self._db, member, name=name, email=email, phone=phone)
