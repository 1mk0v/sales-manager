import datetime as dt
import database as db
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

    def getInitials(self):
        logger.debug("Getting initials...")
        return f"{self.surename} {self.name[0]}.{self.patronomic[0]}."

    async def getSoldProducts(
            self, 
            connection:db.asyncpg.Connection = None, 
            startDate:dt.date =  None,
            endDate:dt.date =dt.date.today()
    ):
        if not connection:
            connection = await db.getConnection()
        if not startDate:
            startDate = endDate - dt.timedelta(days=30)
        logger.debug(f"Get products sold by manager {self.id} in ({startDate.isoformat()} - {endDate.isoformat()})")
        try:
            return await connection.fetchval(
                """
                    SELECT SUM(amount)
                    FROM sales 
                    WHERE dt_rep >= $1 and dt_rep <= $2 and manag_id = $3;
                """,
                startDate,
                endDate,
                self.id
            )
        except Exception as err:
            logger.critical(err)
            exc.BaseAPIException(message="Something wrong with app!", status_code=500)

    async def getSalesPlan(
            self, 
            connection:db.asyncpg.Connection = None,
            month:int = dt.date.today().month
    ):
        if not connection:
            connection = await db.getConnection()
        logger.debug(f"Get sales plan by manager {self.id} at month num {month}")
        try:
            return await connection.fetchval(
                """
                    SELECT *
                    FROM sales 
                    WHERE dt_rep >= $1 and dt_rep <= $2 and manag_id = $3;
                """,
                self.id
            )
        except Exception as err:
            logger.critical(err)
            exc.BaseAPIException(message="Something wrong with app!", status_code=500)
            

    async def getManagerDashboard(self):
        if self.roleName != 'manager':
            raise exc.NoAccessRights()
        conn = await db.getConnection()
        try:
            soldedProducts = await self.getSoldProducts(conn)
            logger.debug(soldedProducts)
        except Exception as err:
            logger.critical(err)
            exc.BaseAPIException(message="Something wrong with app!", status_code=500)

    async def getDashboardInfo(self):
        pass


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
