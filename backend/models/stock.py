from pydantic import BaseModel

class StockInfoRequest(BaseModel):
    name: str


class StockInfoResponse(BaseModel):
    api_res: int
    code: int
    name: str
    market: str