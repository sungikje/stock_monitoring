# Lib import
from fastapi import APIRouter
from typing import List

# Project import
from backend.models.stock import (
    StockInfoResponse,
    CreateFavoriteCompany,
    DeleteFavoriteCompany,
)
from backend.services.stock_service import (
    search_company,
    search_user_favorite_company,
    create_favorite_company,
    delete_favorite_company,
    stock_monitoring,
)
from backend.models.user import UserSearchUseEmail
from backend.models.stock import SearchFavoriteCompany

router = APIRouter()


@router.post("/search_company")
def api_search_company(company_name: str) -> List[StockInfoResponse]:
    return search_company(company_name)


@router.post("/search_favorite_company")
async def api_search_user_favorite_company(
    user: UserSearchUseEmail,
) -> List[SearchFavoriteCompany]:
    return await search_user_favorite_company(user)


@router.post("/create_favorite_company")
async def api_create_favorite_company(create_info: CreateFavoriteCompany):
    return await create_favorite_company(create_info)


@router.post("/delete_favorite_company")
async def api_delete_favorite_company(delete_info: DeleteFavoriteCompany):
    return await delete_favorite_company(delete_info)


@router.post("/stock_monitoring")
async def api_stock_monitoring(user: UserSearchUseEmail):
    return await stock_monitoring(user)
