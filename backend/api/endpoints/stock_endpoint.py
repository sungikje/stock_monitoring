# Lib import
from fastapi import APIRouter
from typing import List
from fastapi import Request

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
from backend.models.stock import SearchFavoriteCompany, SearchCompany, CreateFavoriteCompanyList

router = APIRouter()


@router.post("/search_company")
def api_search_company(request: SearchCompany) -> List[StockInfoResponse]:
    return search_company(request.company_name)


@router.post("/search_favorite_company")
async def api_search_user_favorite_company(
    request: Request
) -> List[SearchFavoriteCompany]:
    user = request.state.user
    return await search_user_favorite_company(user['email'])


@router.post("/create_favorite_company")
async def api_create_favorite_company(request: Request, create_info: CreateFavoriteCompanyList):
    user = request.state.user
    return await create_favorite_company(user['user_id'], create_info.company_list)


@router.post("/delete_favorite_company")
async def api_delete_favorite_company(delete_info: DeleteFavoriteCompany):
    return await delete_favorite_company(delete_info)


@router.post("/stock_monitoring")
async def api_stock_monitoring(user: UserSearchUseEmail):
    return await stock_monitoring(user)
