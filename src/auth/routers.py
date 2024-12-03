from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from exceptions import BaseAPIException
from models import Response
from .depends import oauth2Scheme
from .manager import Authentificator, UsersPasswordsManager, UserSessionsManager
from .models import Token, LoginResponse
from .config import SECRET_KEY, ALGORITHM
from core.users import UserAuth
from jwt.exceptions import InvalidTokenError
import jwt
import logging

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

async def get_current_user(token: Annotated[str, Depends(oauth2Scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.debug("Getting current user...")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Could not validate credentials!")
            raise credentials_exception
    except InvalidTokenError as err:
        logger.warning(f"Abort! {err}")
        raise credentials_exception
    
    userPswdManager = UsersPasswordsManager()
    user = await userPswdManager.getUserAuthByLogin(username)
    if user is None:
        raise credentials_exception
    return UserAuth(user.login, user.passwordHash, user.userId, token)


async def get_current_active_user(
    currentUser: Annotated[UserAuth, Depends(get_current_user)],
):
    logger.info(f"Getting current active user...")
    userSessionManager = UserSessionsManager()
    currentUserSession = await userSessionManager.getCurrentUserSession(currentUser.userId)
    if not currentUserSession or not currentUser.isSessionsEqual(currentUserSession):
        raise HTTPException(status_code=400, detail="Inactive user")
    logger.info(f"Success")
    return currentUser


@router.post("/token", summary="GET token")
async def getToken(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token | Response:
    try:
        sessionManager = Authentificator()
        token = await sessionManager.getSessionForUser(login=data.username, password=data.password)
        return token
    except BaseAPIException as err:
        return Response(
            status=err.status_code,
            detail=err.message,
            data=None
        )

@router.get("/me", summary="Get response", response_model=LoginResponse)
async def read_users_me(
    currentUser: Annotated[UserAuth, Depends(get_current_active_user)],
):
    return Response(data=currentUser.login)


@router.post('/logout', summary="Drop token", response_model=LoginResponse)
async def dropToken(
    currentUser: Annotated[UserAuth, Depends(get_current_active_user)],
):  
    if await UserSessionsManager().dropSession(currentUser.getSession):
        return LoginResponse(data=currentUser.login)