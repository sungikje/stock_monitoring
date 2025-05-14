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
async def api_search_user_favorite_company() -> List[SearchFavoriteCompany]:
    return await search_user_favorite_company("admin@example.com")

@log_call
@router.post("/create_favorite_company")
async def api_create_favorite_company(create_info: CreateFavoriteCompanyList):
    return await create_favorite_company(1, create_info.company_list)

@log_call
@router.post("/delete_favorite_company")
async def api_delete_favorite_company(company_info: CompanyInfo):
    return await delete_favorite_company(1, company_info)

@log_call
@router.post("/stock_monitoring")
async def api_stock_monitoring() -> List[ViewChart]:
    return await get_view_chart("admin@example.com")

@log_call
@router.post("/update_favorite_company_industry_period")
async def api_update_favorite_company_industry_period(update_info: UpdateIndustryInfo):
    return await update_favorite_company_industry_period("admin@example.com", update_info)
