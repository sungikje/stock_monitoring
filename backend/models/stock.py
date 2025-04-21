from pydantic import BaseModel
from datetime import datetime
from typing import List

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


class SearchCompany(BaseModel):
    company_name: str


class FavoriteCompanyInfo(BaseModel):
    company_name: str

class CreateFavoriteCompanyList(BaseModel):
    company_list: List[FavoriteCompanyInfo]

class DeleteFavoriteCompany(BaseModel):
    user_id: str
    company_name: str


class ViewChart(BaseModel):
    company_name: str
    save_path: str

class UpdateIndustryInfo(BaseModel):
    company_name: str
    industry_period: str