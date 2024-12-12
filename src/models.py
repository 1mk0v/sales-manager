from pydantic import BaseModel
from typing import Dict, List, Any

class Response(BaseModel):
    status: int = 200
    detail: str = "success"
    data: Dict | List | Any | None


class SalesPlan(BaseModel):
    sales_amount:int | None = None
    new_clients:int | None = None

class SalesAmountResponse(Response):
    data:SalesPlan