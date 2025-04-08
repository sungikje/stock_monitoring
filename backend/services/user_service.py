# Lib import
from backend.db.connection import get_pool
from pydantic import EmailStr
import aiomysql
from typing import List

# Project import
from backend.models.user import UserResponse, UserSearch
from backend.models.stock import FavoriteCompany


async def search_user_favorite_company(user: UserSearch) -> List[FavoriteCompany]:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            user_row = await cur.fetchone()

            if not user_row:
                return None

            user_response = UserResponse(**user_row)

            await cur.execute(
                "SELECT * FROM user_favorite_companies WHERE user_id = %s", 
                (user_response.id,)
            )
            favorite_rows = await cur.fetchall()

            # 리스트로 가공해서 추가
            favorite_companies = [FavoriteCompany(**row) for row in favorite_rows]

            return favorite_companies