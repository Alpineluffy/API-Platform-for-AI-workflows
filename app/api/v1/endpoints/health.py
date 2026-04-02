from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Liveness / readiness probe."""
    return {
        "status": "healthy",
        "version": "1.0.0",
    }
