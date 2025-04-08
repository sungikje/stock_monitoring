# Lib import
from fastapi import APIRouter
from pydantic import EmailStr

# Project import
from backend.models.user import UserResponse, UserSearch
from backend.services.user_service import search_user

router = APIRouter()

@router.post("/search_user")
async def api_search_user(user: UserSearch) -> UserResponse:
    print("endpoint come in")
    return await search_user(user)
