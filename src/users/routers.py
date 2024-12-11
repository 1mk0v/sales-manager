from fastapi import APIRouter, Depends
from auth.routers import get_current_active_user
from models import Response
from .models import BaseUserInfoResponse, BaseUserInfo
from typing import Annotated
from core import users
import logging

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get("/me", summary="Get info about user", response_model=BaseUserInfoResponse)
async def getInfoAboutMe(currentUser: Annotated[users.UserAuth, Depends(get_current_active_user)]):
    user = await currentUser.getUser()
    return Response(data=BaseUserInfo(
        initials=user.getInitials(),
        role=user.roleName
        )
    )

@router.get("/manager/dashboard", summary="Get dashboard info for manager")
async def getDashboardInfo(currentUser: Annotated[users.UserAuth, Depends(get_current_active_user)]):
    user = await currentUser.getUser()
    return Response(data=(await user.getSoldProducts()))
# @router.get("")