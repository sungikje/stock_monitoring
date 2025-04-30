# Lib import
from fastapi import APIRouter

# Project import
from backend.models.user import UserCreateInfo, UserLoginInfo
from backend.services.user_service import user_login, user_join_membership

from backend.config.logging import log_call

router = APIRouter()

@log_call
@router.post("/signup")
async def api_user_join_membership(user_info: UserCreateInfo):
    return await user_join_membership(user_info)

@log_call
@router.post("/login")
async def api_user_login(login_info: UserLoginInfo):
    return await user_login(login_info)
