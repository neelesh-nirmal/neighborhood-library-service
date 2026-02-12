"""Seed the database with books, members, and book copies (one script for all static data).

Run from apis/:
  uv run python scripts/seed_data.py
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Book, Member
from app.repositories.book_copy_repository import BookCopyRepository
from app.repositories.book_repository import BookRepository
from app.repositories.member_repository import MemberRepository

# ---- Books ----
SEED_BOOKS = [
    {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "description": "The big ideas behind reliable, scalable, and maintainable systems.",
        "isbn": "978-1449373320",
    },
    {
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "description": "A craftsman's guide to software structure and design.",
        "isbn": "978-0134494166",
    },
    {
        "title": "Building Microservices",
        "author": "Sam Newman",
        "description": "Designing fine-grained systems.",
        "isbn": "978-1492034025",
    },
    {
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell, Peter Norvig",
        "description": "The long-anticipated revision of the definitive AI textbook.",
        "isbn": "978-0136042594",
    },
    {
        "title": "Deep Learning",
        "author": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
        "description": "Adaptive computation and machine learning.",
        "isbn": "978-0262035613",
    },
    {
        "title": "Patterns of Enterprise Application Architecture",
        "author": "Martin Fowler",
        "description": "Describes patterns for the design of enterprise applications.",
        "isbn": "978-0321127426",
    },
    {
        "title": "Domain-Driven Design",
        "author": "Eric Evans",
        "description": "Tackling complexity in the heart of software.",
        "isbn": "978-0321125217",
    },
    {
        "title": "The Phoenix Project",
        "author": "Gene Kim, Kevin Behr, George Spafford",
        "description": "A novel about IT, DevOps, and helping your business win.",
        "isbn": "978-0988262591",
    },
    {
        "title": "Site Reliability Engineering",
        "author": "Betsy Beyer et al.",
        "description": "How Google runs production systems.",
        "isbn": "978-1491929124",
    },
    {
        "title": "Machine Learning Yearning",
        "author": "Andrew Ng",
        "description": "Technical strategy for AI projects.",
        "isbn": None,
    },
    {
        "title": "Fundamentals of Software Architecture",
        "author": "Mark Richards, Neal Ford",
        "description": "An engineering approach to software design.",
        "isbn": "978-1492043454",
    },
    {
        "title": "Release It!",
        "author": "Michael T. Nygard",
        "description": "Design and deploy production-ready software.",
        "isbn": "978-1680502398",
    },
]

# ---- Members ----
SEED_MEMBERS = [
    {"name": "Alice Chen", "email": "alice.chen@example.com", "phone": "+1-555-0101"},
    {"name": "Bob Martinez", "email": "bob.martinez@example.com", "phone": "+1-555-0102"},
    {"name": "Carol Okonkwo", "email": "carol.o@example.com", "phone": None},
    {"name": "David Park", "email": "david.park@example.com", "phone": "+1-555-0104"},
    {"name": "Eva Schmidt", "email": "eva.schmidt@example.com", "phone": "+1-555-0105"},
]

# ---- Copies: (book title, copy_code). Book must exist (from SEED_BOOKS). ----
SEED_COPIES = [
    ("Designing Data-Intensive Applications", "DDIA-001"),
    ("Designing Data-Intensive Applications", "DDIA-002"),
    ("Clean Architecture", "CA-001"),
    ("Building Microservices", "BM-001"),
    ("Artificial Intelligence: A Modern Approach", "AIMA-001"),
    ("Deep Learning", "DL-001"),
    ("Deep Learning", "DL-002"),
    ("Domain-Driven Design", "DDD-001"),
    ("The Phoenix Project", "TPP-001"),
    ("Site Reliability Engineering", "SRE-001"),
    ("Fundamentals of Software Architecture", "FSA-001"),
    ("Release It!", "RI-001"),
]


def main() -> None:
    db = SessionLocal()
    book_repo = BookRepository()
    member_repo = MemberRepository()
    copy_repo = BookCopyRepository()

    # Build title -> book_id for all books (existing + created)
    def book_id_by_title(title: str):
        row = db.execute(select(Book).where(Book.title == title)).scalar_one_or_none()
        return row.id if row else None

    try:
        # --- Books ---
        logger.info("Books")
        books_created = 0
        for data in SEED_BOOKS:
            if db.execute(select(Book).where(Book.title == data["title"])).scalar_one_or_none():
                continue
            book_repo.create(
                db,
                title=data["title"],
                author=data["author"],
                description=data.get("description"),
                isbn=data.get("isbn"),
            )
            books_created += 1
            logger.info("  + %s", data["title"])
        logger.info("  Created %s books.\n", books_created)

        # --- Members ---
        logger.info("Members")
        members_created = 0
        for data in SEED_MEMBERS:
            existing = db.execute(
                select(Member).where(Member.email == data["email"])
            ).scalar_one_or_none()
            if existing:
                continue
            member_repo.create(
                db,
                name=data["name"],
                email=data["email"],
                phone=data.get("phone"),
            )
            members_created += 1
            logger.info("  + %s", data["name"])
        logger.info("  Created %s members.\n", members_created)

        # --- Copies ---
        logger.info("Copies")
        copies_created = 0
        for book_title, copy_code in SEED_COPIES:
            if copy_repo.get_by_copy_code(db, copy_code):
                continue
            bid = book_id_by_title(book_title)
            if not bid:
                logger.warning("  Skip %s: book '%s' not found", copy_code, book_title)
                continue
            copy_repo.create(db, book_id=bid, copy_code=copy_code)
            copies_created += 1
            logger.info("  + %s (%s)", copy_code, book_title)
        logger.info("  Created %s copies.\n", copies_created)

        logger.info("Done.")
    except Exception as e:
        logger.exception("Seed failed: %s", e)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
