"""Route modules."""

from app.api.routes.books import router as books_router
from app.api.routes.health import router as health_router
from app.api.routes.loans import router as loans_router
from app.api.routes.members import router as members_router

__all__ = [
    "books_router",
    "health_router",
    "loans_router",
    "members_router",
]
