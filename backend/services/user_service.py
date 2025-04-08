# Lib import
from backend.db.connection import get_pool
from pydantic import EmailStr
import aiomysql

# Project import
from backend.models.user import UserResponse, UserSearch


async def find_user_by_email(user: UserSearch) -> UserResponse:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            user_row = await cur.fetchone()

            if not user_row:
                return None

            user_response = UserResponse(**user_row)
    return user_response