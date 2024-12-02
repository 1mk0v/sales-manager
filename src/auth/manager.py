import database as db
from database.models import users 
import logging
from passlib.context import CryptContext
from . import TokenCreater
from .config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from .exceptions import NotFoundUserError, AuthException, IncorrectPasswordError

logger = logging.getLogger('uvicorn.error')


class UsersPasswordsManager():

    def __init__(self) -> None:
        self.pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def getUserAuthByLogin(self, login:str):
        conn = await db.getConnection()
        try:
            result = await conn.fetchrow("""SELECT * FROM user_auth where login = $1""", login)
            logger.debug(f"SELECT user_auth {result}")
            if result == None:
                raise NotFoundUserError(status_code=404, message=f"Not found user with login {login}")
            return users.UserAuth(login=result['login'], passwordHash=result['password_hash'], userId=result['user_id'])
        except Exception as err:
            logger.warn(err)
            raise AuthException()
        finally:
            await conn.close()

    async def authenticationUser(self, login:str, password:str):
        userAuth = await self.getUserAuthByLogin(login)
        logger.debug(f"Verifing password for {userAuth.login}")
        if not self.verifyPassword(password, userAuth.passwordHash):
            raise IncorrectPasswordError(
                status_code=400,
                message=f"Incorrect password for user {login}"
            )
        return True

    def getPasswordHash(self, password:str):
        return self.pwdContext.hash(password)
    
    def verifyPassword(self, password:str, passwordHash:str):
        return self.pwdContext.verify(password, passwordHash)

class UserSessionsManager():
    
    def __init__(self) -> None:
        pass


class AuthManager():

    def __init__(self) -> None:
        self.tokenCreater = TokenCreater(
            secret_key=SECRET_KEY, 
            algorithm=ALGORITHM, 
            validity=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        self.userManager = UsersPasswordsManager()

    async def getToken(self, login, password):
        await self.userManager.authenticationUser(login=login, password=password)
        return self.tokenCreater.getJWT(login)