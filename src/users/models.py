from pydantic import BaseModel
from models import Response

class BaseUserInfo(BaseModel):
    initials:str
    role:str

class BaseUserInfoResponse(Response):
    data:BaseUserInfo