# Lib import
from fastapi import APIRouter

# Project import
from backend.models.user import UserCreateInfo, UserLoginInfo
from backend.services.user_service import user_login, user_join_membership

router = APIRouter()


@router.post("/user_join")
async def api_user_join_membership(user_info: UserCreateInfo):
    return await user_join_membership(user_info)


@router.post("/user_login")
async def api_user_login(login_info: UserLoginInfo):
    return await user_login(login_info)
