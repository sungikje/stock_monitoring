# Lib import
from backend.db.connection import get_pool
import aiomysql
import bcrypt

# Project import
from backend.models.user import (
    UserResponse,
    UserLoginInfo,
    UserCreateInfo,
)
from backend.utils.jwt import create_access_token
from backend.config.logging import log_call

@log_call
async def find_user_by_email(user_email: str) -> UserResponse:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM users WHERE email = %s", (user_email,))
            user_row = await cur.fetchone()

            if not user_row:
                return None

            user_response = UserResponse(**user_row)
    return user_response

@log_call
async def user_join_membership(user_info: UserCreateInfo):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM users WHERE email = %s", (user_info.email,)
            )
            user_row = await cur.fetchone()

            if not user_row:
                password_bytes = user_info.password.encode("utf-8")
                password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode(
                    "utf-8"
                )

                await cur.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (user_info.username, user_info.email, password_hash),
                )
                await conn.commit()
                return {"status": "success", "message": "join with us"}
            else:
                return {"status": "error", "message": "already exist user"}

@log_call
async def user_login(login_info: UserLoginInfo):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM users WHERE email = %s", (login_info.email,)
            )
            user_row = await cur.fetchone()

            if not user_row:
                return {"status": "error", "message": "no user"}

            password_hash = user_row["password_hash"].encode(
                "utf-8"
            )  # DB에 저장된 해시

    password_bytes = login_info.password.encode("utf-8")

    if bcrypt.checkpw(password_bytes, password_hash):
        token = create_access_token(
            {"user_id": user_row["id"], "email": user_row["email"]}
        )
        return {"status": "success", "message": "issue token", "access_token": token}
    else:
        return {"status": "error", "message": "wrong password"}
