"""Health check route - single responsibility: expose health status."""

from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns service health status for load balancers and monitoring.",
)
def get_health() -> HealthResponse:
    """Return health status and API version."""
    return HealthResponse(status="ok", version="0.1.0")
