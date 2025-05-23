# Lib import
from fastapi import APIRouter
from typing import List, Union
from fastapi import Request

# Project import
from backend.models.stock import StockInfoResponse, CompanyInfo, ViewChart
from backend.services.stock_service import (
    search_company,
    search_user_favorite_company,
    create_favorite_company,
    delete_favorite_company,
    get_view_chart,
    update_favorite_company_industry_period
)
from backend.models.stock import (
    SearchFavoriteCompany,
    CompanyInfo,
    CreateFavoriteCompanyList,
    UpdateIndustryInfo,
)

from backend.config.logging import log_call

router = APIRouter()

@log_call
@router.post("/search_company")
def api_search_company(request: CompanyInfo) -> Union[List[StockInfoResponse], dict]:
    return search_company(request.company_name)

@log_call
@router.post("/search_favorite_company")
async def api_search_user_favorite_company(
    request: Request,
) -> List[SearchFavoriteCompany]:
    user = request.state.user
    return await search_user_favorite_company(user["email"])

@log_call
@router.post("/create_favorite_company")
async def api_create_favorite_company(
    request: Request, create_info: CreateFavoriteCompanyList
):
    user = request.state.user
    return await create_favorite_company(user["user_id"], create_info.company_list)

@log_call
@router.post("/delete_favorite_company")
async def api_delete_favorite_company(
    request: Request, company_info: CompanyInfo
):
    user = request.state.user
    return await delete_favorite_company(user["user_id"], company_info)

@log_call
@router.post("/stock_monitoring")
async def api_stock_monitoring(request: Request) -> List[ViewChart]:
    user = request.state.user
    return await get_view_chart(user["email"])

@log_call
@router.post("/update_favorite_company_industry_period")
async def api_update_favorite_company_industry_period(
    request: Request, update_info: UpdateIndustryInfo
):
    user = request.state.user
    return await update_favorite_company_industry_period(user["email"], update_info)
