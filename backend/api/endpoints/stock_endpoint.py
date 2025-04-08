# Lib import
from fastapi import APIRouter
from typing import List

# Project import
from backend.models.stock import StockInfoResponse, DeleteFavoriteCompany
from backend.services.stock_service import search_company, search_user_favorite_company, delete_company
from backend.models.user import UserSearch
from backend.models.stock import SearchFavoriteCompany

router = APIRouter()

@router.post("/search_company")
def api_search_company(company_name: str) -> List[StockInfoResponse]:
    return search_company(company_name)

@router.post("/search_favorite_company")
async def api_search_user_favorite_company(user: UserSearch) -> List[SearchFavoriteCompany]:
    return await search_user_favorite_company(user)

@router.post("/delete_favorite_company")
async def api_delete_company(delete_info: DeleteFavoriteCompany):
    return await delete_company(delete_info)