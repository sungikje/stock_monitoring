# Lib import
from fastapi import APIRouter
from typing import List

# Project import
from backend.models.stock import StockInfoResponse
from backend.services.stock_service import search_company

router = APIRouter()

@router.post("/search_company")
def api_search_company(company_name: str) -> List[StockInfoResponse]:
    return search_company(company_name)
