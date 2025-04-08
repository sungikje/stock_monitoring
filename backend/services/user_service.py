# Lib import
from backend.db.connection import get_pool
from pydantic import EmailStr
import aiomysql

# Project import
from backend.models.user import UserResponse, UserSearch


async def search_user(user: UserSearch) -> UserResponse:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            row = await cur.fetchone()
            print(row)
            if row:
                return UserResponse(**row)
            return None