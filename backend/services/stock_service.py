# Lib import
from fastapi import HTTPException
import FinanceDataReader as fdr
from typing import List
import aiomysql

# Project import
from backend.db.connection import get_pool
from backend.models.user import UserSearch
from backend.services.user_service import find_user_by_email
from backend.models.stock import StockInfoResponse, SearchFavoriteCompany, CreateFavoriteCompany, DeleteFavoriteCompany


def search_company(name: str) -> List[StockInfoResponse]:

	krx_stocks = fdr.StockListing('KRX')
	company_info = krx_stocks[krx_stocks['Name'].str.contains(name, case=False, na=False)]

	if company_info.empty:
		print('error')
		raise HTTPException(status_code=404, detail="Company not found")

	result = [
		StockInfoResponse(
			code=row['Code'],
			name=row['Name'],
			market=row['Market']
		)
		for _, row in company_info.iterrows()
	]

	return result


async def search_user_favorite_company(user: UserSearch) -> List[SearchFavoriteCompany]:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            user_response = await find_user_by_email(user)

            await cur.execute("SELECT * FROM user_favorite_companies WHERE user_id = %s", 
                (user_response.id,)
            )
            favorite_rows = await cur.fetchall()

            favorite_companies = [SearchFavoriteCompany(**row) for row in favorite_rows]

            return favorite_companies


async def delete_company(delete_info: DeleteFavoriteCompany):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM user_favorite_companies WHERE user_id = %s AND company_name = %s", 
                (delete_info.user_id, delete_info.company_name)
            )
            
            delete_tf = await cur.fetchall()
            if not delete_tf:
                return {"error": "error", "message": "fail find favorite company"}

            await cur.execute(
                "DELETE FROM user_favorite_companies WHERE user_id = %s AND company_name = %s", 
                (delete_info.user_id, delete_info.company_name)
            )
            await conn.commit()
            return {"result": "success"}

async def create_favorite_company(create_info: CreateFavoriteCompany):
     pool = get_pool()
     async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM user_favorite_companies WHERE user_id = %s AND company_name = %s", 
                (create_info.user_id, create_info.company_name)
            )
            
            delete_tf = await cur.fetchall()
            if delete_tf:
                return {"error": "error", "message": "already exist company list"}

            await cur.execute(
                "INSERT INTO user_favorite_companies (user_id, company_name, industry_period, base_price) VALUES (%s, %s, 2, 50000)", 
                (create_info.user_id, create_info.company_name)
            )
            await conn.commit()
            return {"result": "success"}