from pydantic import BaseModel
from datetime import datetime

class StockInfoRequest(BaseModel):
    name: str


class StockInfoResponse(BaseModel):
    code: str
    name: str
    market: str

class SearchFavoriteCompany(BaseModel):
    id: int
    user_id: int
    company_name: str
    industry_period: int
    base_price: int
    created_at: datetime

class CreateFavoriteCompany(BaseModel):
    user_id: str
    company_name: str

class DeleteFavoriteCompany(BaseModel):
    user_id: str
    company_name: str