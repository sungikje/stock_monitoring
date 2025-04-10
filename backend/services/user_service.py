# Lib import
from backend.db.connection import get_pool
from pydantic import EmailStr
import aiomysql

# Project import
from backend.models.user import UserResponse, UserSearchUseEmail


async def find_user_by_email(user: UserSearchUseEmail) -> UserResponse:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            user_row = await cur.fetchone()

            if not user_row:
                return None

            user_response = UserResponse(**user_row)
    return user_response

async def user_email_to_id(user: UserSearchUseEmail) -> str:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            user_row = await cur.fetchone()

            if not user_row:
                return None

            user_id = UserResponse(**user_row).id
    return user_id