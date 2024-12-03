from pydantic import BaseModel
from models import Response


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class TokenResponse(Response):
    data:Token

class LoginResponse(Response):
    data:str