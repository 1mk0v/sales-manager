import database as db
import datetime as dt
import core.metrics as metrics
import core.exceptions as exc
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
        self.numMetric = metrics.NumericMetrics(self.id)

    def getInitials(self):
        logger.debug("Getting initials...")
        return f"{self.surename} {self.name[0]}.{self.patronomic[0]}."

    async def getManagerDashboard(self, date:dt.date):
        if self.roleName != 'manager':
            raise exc.NoAccessRights()
        conn = await db.getConnection()
        try:
            logger.debug(f"GET sales plan {await self.numMetric.getSalesPlan(conn)}")
            logger.debug(f"GET sold products {await self.numMetric.getSoldProducts(conn)}")
            logger.debug(f"GET new customers {await self.numMetric.getUserNewCustomers(conn)}")
            return "success"
        except Exception as err:
            logger.critical(err)
            exc.BaseAPIException(message="Something wrong with app!", status_code=500)

    async def getDashboardInfo(self, date:dt.date):
        if self.roleName == 'manager':
            return await self.getManagerDashboard(date)
        else:
            return None


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
