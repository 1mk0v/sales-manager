import database as db
import logging

logger = logging.getLogger("uvicorn.error")

class User():

    def __init__(self, id:int, name:str, surename:str, patronomic:str, role:str, office_id:str) -> None:
        self.id = id
        self.name = name
        self.surename = surename
        self.patronomic = patronomic
        self.roleName = role
        self.officeId = office_id

    def getInitials(self):
        logger.debug("Getting initials...")
        return f"{self.surename} {self.name[0]}.{self.patronomic[0]}."
    
    async def getHashedAuthInfo(self):
        logger.debug("Getting user authentification info...")
        conn = await db.getConnection()
        conn.fetchrow("""SELECT * FROM user_auth as where id = $1""", self.id)


class UserAuth():
    def __init__(self, login:str, passwordHash:str, userId:int, session:str = None):
        self.login = login
        self.passwordHash = passwordHash
        self.userId = userId
        self.__session = session
    
    def isSessionsEqual(self, session:str):
        return self.__session == session
    
    async def getUser(self):
        conn = await db.getConnection()
        userResult = await conn.fetchrow('''SELECT * FROM managers where id = $1''', self.userId)
        logger.debug(f"Get user by id = {self.userId}")
        return User(
            id=userResult["id"], name=userResult["name"], surename=userResult["surename"],
            patronomic=userResult["patronomic"], role=userResult["role"], office_id=userResult["office_id"]
        )
        
    @property
    def getSession(self):
        logger.debug("Getting session...")
        return self.__session
