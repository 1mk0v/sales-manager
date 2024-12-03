import database as db
from asyncpg import Connection
from core import users 
import logging
from passlib.context import CryptContext
from datetime import timedelta
from . import TokenCreater
from .models import Token
from .config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from .exceptions import NotFoundUserError, AuthException, IncorrectPasswordError

logger = logging.getLogger('uvicorn.error')


class UsersPasswordsManager():

    def __init__(self, connection:Connection = None) -> None:
        self.pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.conn = connection

    async def getUserAuthByLogin(self, login:str):
        logger.debug(f"Get user authentication info by login...")
        conn = await db.getConnection()
        try:
            result = await conn.fetchrow("""SELECT * FROM user_auth where login = $1""", login)
            if result == None:
                logger.warning(f"User {login} not found! Abort!")
                raise NotFoundUserError(status_code=404, message=f"Not found user with login {login}")
            logger.debug(f"Success!")
            return users.UserAuth(login=result['login'], passwordHash=result['password_hash'], userId=result['user_id'])
        except Exception as err:
            logger.warning(f'Abort! {err}')
            raise AuthException()
        finally:
            await conn.close()
            logger.debug(f"Connection close")

    async def authenticationUser(self, login:str, password:str):
        logger.debug(f"Authentication user {login}...")
        userAuth = await self.getUserAuthByLogin(login)
        if not self.verifyPassword(password, userAuth.passwordHash):
            logger.warning(f"Incorrect password")
            raise IncorrectPasswordError(
                status_code=400,
                message=f"Incorrect password for user {login}"
            )
        logger.debug(f"Authenticated")
        return userAuth

    def getPasswordHash(self, password:str):
        logger.debug(f"Hashing password...")
        return self.pwdContext.hash(password)
    
    def verifyPassword(self, password:str, passwordHash:str):
        logger.debug(f"Verifing password...")
        return self.pwdContext.verify(password, passwordHash)

class UserSessionsManager():
    
    def __init__(self) -> None:
        self.tokenCreater = TokenCreater(
            secret_key=SECRET_KEY, 
            algorithm=ALGORITHM, 
            validity=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    
    async def getCurrentUserSession(self, userId) -> str:
        logger.debug(f"Get session for user_id {userId}")
        conn = await db.getConnection()
        try:
            result =  await conn.fetchval(
                '''
                SELECT session 
                FROM user_session 
                WHERE user_id = $1 and EXTRACT(EPOCH FROM (now()::timestamp-logined)/60) < $2 and is_active = TRUE
                ''',
                userId, int(ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            logger.debug(f'Recieved session')
            return result
        except Exception as err:
            logger.warning(f'{err}')
        finally:
            await conn.close()
            logger.debug(f"Connection close")

    async def createSession(self, login, userId) -> str:
        logger.debug(f"Creating session...")
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
        except Exception as err:
            logger.warning(f'Abort! {err}')
        finally:
            await conn.close()
            logger.debug(f"Connection close")
        
    async def dropSession(self, session):
        logger.debug(f"Droping session...")
        conn = await db.getConnection()
        try:
            return await conn.fetchval(
                """
                UPDATE user_session 
                SET is_active = FALSE 
                WHERE session = $1
                RETURNING user_id
                """,
                session
            )
        except Exception as err:
            logger.warning(f'Abort! {err}')
        finally:
            await conn.close()
            logger.debug(f"Connection close")


class Authentificator():
    
    def __init__(self) -> None:
        self.usersPasswordsManager = UsersPasswordsManager()
        self.usersSessionsManager = UserSessionsManager()

    async def getSessionForUser(self, login:str, password:str):
        logger.info("Getting session...")
        userAuth = await self.usersPasswordsManager.authenticationUser(login, password)
        session = await self.usersSessionsManager.getCurrentUserSession(userAuth.userId)
        if not session:
            logger.info("Session not found. Creating...")
            session = await self.usersSessionsManager.createSession(login, userId=userAuth.userId)
            logger.info("Created session!")
        return Token(access_token=session)