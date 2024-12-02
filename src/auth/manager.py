import database as db
from database.models import users 
import logging
from passlib.context import CryptContext
from datetime import timedelta
from . import TokenCreater
from .models import Token
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
        return userAuth

    def getPasswordHash(self, password:str):
        return self.pwdContext.hash(password)
    
    def verifyPassword(self, password:str, passwordHash:str):
        return self.pwdContext.verify(password, passwordHash)


class UserSessionsManager():
    
    def __init__(self) -> None:
        self.tokenCreater = TokenCreater(
            secret_key=SECRET_KEY, 
            algorithm=ALGORITHM, 
            validity=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
    
    async def getCurrentUserSession(self, userId) -> str:
        conn = await db.getConnection()
        try:
            logger.debug(f"Get current session of {userId}")
            result = await conn.fetchval(
                '''
                SELECT session 
                FROM user_session 
                where user_id = $1 and EXTRACT(EPOCH FROM (now()::timestamp-logined)/60) < $2 and is_active = TRUE
                ''',
                userId, int(ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            logger.debug(f"User session {result}")
            return result
        except Exception as err:
            logger.warn(err)
        finally:
            await conn.close()

    async def createSession(self, login, userId) -> str:
        token = self.tokenCreater.getJWT(username=login)
        conn = await db.getConnection()
        try:
            return await conn.fetchval(
                '''
                INSERT INTO user_session (session, user_id)
                VALUES ($1, $2)
                RETURNING session
                ''', token.access_token, userId
            )
        except Exception as error:
            logger.warning(error)
        finally:
            await conn.close()
        
    async def dropSession(self, userId):
        conn = await db.getConnection()
        pass

class Authentificator():
    
    def __init__(self) -> None:
        self.usersPasswordsManager = UsersPasswordsManager()
        self.usersSessionsManager = UserSessionsManager()

    async def getSessionForUser(self, login:str, password:str):
        userAuth = await self.usersPasswordsManager.authenticationUser(login, password)
        session = await self.usersSessionsManager.getCurrentUserSession(userAuth.userId)
        if not session:
            session = await self.usersSessionsManager.createSession(login, userId=userAuth.userId)
        logger.debug(f"Session {session}")
        return Token(access_token=session)