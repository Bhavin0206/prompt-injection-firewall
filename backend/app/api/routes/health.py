"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """Simple liveness check."""
    return {"status": "ok", "service": "prompt-injection-firewall"}
