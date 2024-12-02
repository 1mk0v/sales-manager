from pydantic import BaseModel
from typing import Dict, List, Any

class Response(BaseModel):
    status: int = 200
    detail: str = "success"
    data: Dict | List | Any | None
