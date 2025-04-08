# Lib import
from fastapi import APIRouter
from pydantic import EmailStr
from typing import List

# Project import
from backend.models.user import UserResponse, UserSearch
from backend.models.stock import FavoriteCompany
from backend.services.user_service import search_user_favorite_company

router = APIRouter()

@router.post("/search_favorite_company")
async def api_search_user_favorite_company(user: UserSearch) -> List[FavoriteCompany]:
    return await search_user_favorite_company(user)
