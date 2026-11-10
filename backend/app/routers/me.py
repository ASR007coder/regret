# regret/backend/app/me.py
# backend/app/me.py

from fastapi import APIRouter, Depends

from backend.database.model import User
from backend.schemas.user import MeResponse
from backend.security.dependencies import get_current_user


router = APIRouter(prefix="/me",tags=["My Profile"])


@router.get("/",response_model=MeResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):

    return current_user