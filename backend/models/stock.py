from pydantic import BaseModel

class StockInfoRequest(BaseModel):
    name: str


class StockInfoResponse(BaseModel):
    code: str
    name: str
    market: str