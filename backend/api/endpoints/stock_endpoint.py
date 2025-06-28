# Lib import
from fastapi import APIRouter
from typing import List, Union
from fastapi import Request

# Project import
from backend.models.stock import StockInfoResponse, CompanyInfo, ViewChart
from backend.services.stock_service import (
    search_company,
    search_user_interesting_company,
    create_interesting_company,
    delete_interesting_company,
    get_view_chart,
    update_interesting_company_industry_period,
    create_stock_moniotring_chart
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
@router.post("/search_interesting_company")
async def api_search_user_interesting_company() -> List[SearchFavoriteCompany]:
    return await search_user_interesting_company()

@log_call
@router.post("/create_interesting_company")
async def api_create_interesting_company(create_info: CreateFavoriteCompanyList):
    return await create_interesting_company(1, create_info.company_list)

@log_call
@router.post("/delete_interesting_company")
async def api_delete_favorite_company(company_info: CompanyInfo):
    return await delete_interesting_company(1, company_info)

@log_call
@router.post("/stock_monitoring")
async def api_stock_monitoring() -> List[ViewChart]:
    return await get_view_chart()

@log_call
@router.post("/update_interesting_company_industry_period")
async def api_update_interesting_company_industry_period(update_info: UpdateIndustryInfo):
    return await update_interesting_company_industry_period(update_info)

@log_call
@router.post("/create_stock_monitoring_chart")
async def api_create_stock_monitoring_chart():
    return await create_stock_moniotring_chart()
