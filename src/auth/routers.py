from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from exceptions import BaseAPIException
from models import Response
from .manager import UserSessionsManager
from .models import TokenResponse
import logging

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/token", summary="GET token")
async def getToken(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse | Response:
    try:
        sessionManager = UserSessionsManager()
        token = await sessionManager.getSessionForUser(login=data.username, password=data.password)
        return TokenResponse(data=token)
    except BaseAPIException as err:
        return Response(
            status=err.status_code,
            detail=err.message,
            data=None
        )
