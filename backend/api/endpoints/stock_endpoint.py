from backend.services.stock_service import search_company
from fastapi import APIRouter

from backend.models.stock import StockInfoResponse

router = APIRouter()

@router.post("/search_company")
def api_search_company(company_name: str) -> StockInfoResponse:
    return search_company(company_name)
