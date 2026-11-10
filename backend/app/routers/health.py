# regret/backend/app/routers/health.py

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("/")
def health_check():

    return {
        "status": "success",
        "message": "REGRET API is running"
    }