from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserSearchUseEmail(BaseModel):
    email: str


# 유저 생성용 요청 모델
class UserCreateInfo(BaseModel):
    username: str
    email: EmailStr
    password: str  # 평문 비밀번호 (DB에는 해시로 저장될 것)
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None


# 유저 로그인
class UserLoginInfo(BaseModel):
    email: str
    password: str


# 유저 조회 응답용 모델
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool
    is_admin: bool
    role: str
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None
