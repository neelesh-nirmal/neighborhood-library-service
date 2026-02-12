"""Application factory - creates and configures the FastAPI app (SRP, OCP)."""

from fastapi import FastAPI

from app.api.routes import health_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Neighborhood Library Service",
        description="API for the neighborhood library service",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.include_router(health_router, prefix="/api/v1")
    return app
