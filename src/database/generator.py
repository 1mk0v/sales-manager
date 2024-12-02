import logging
from auth.manager import UsersPasswordsManager
from .schemas import user_session, managers, offices, user_auth
from . import getConnection

logger = logging.getLogger('uvicorn.error')

class DBGenerator():

    def __init__(self) -> None:
        self.schema = {
            "offices": offices,
            "managers": managers,
            "user_auth": user_auth,
            "user_session": user_session
        }
    
    async def generateTables(self):
        conn = await getConnection()
        for key in self.schema:
            try:
                result = await conn.execute(f"""CREATE TABLE {key} ({self.schema[key]})""")
                logger.debug(f"{result} {key}")
            except Exception as err:
                logger.warn(err)
        await conn.close()
    
    async def generateManager(self):
        conn = await getConnection()
        try:
            result = await conn.execute(
                f"""INSERT INTO managers (name, surename, patronomic, office_id, role) 
                    values ('Иван', 'Иванов', 'Иванович', 1, 'manager')"""
            )
            logger.debug(f"{result}")
        except Exception as err:
            logger.warn(err)
        await conn.close()
    
    async def generateOffice():
        conn = await getConnection()
        try:
            result = await conn.execute(
                f"""INSERT INTO offices (id, location) 
                    values (1, 'ул. Колотушкина, д.10')"""
            )
            logger.debug(f"{result}")
        except Exception as err:
            logger.warn(err)
        await conn.close()

    async def generateUserAuth(self):
        pswdManager = UsersPasswordsManager()
        conn = await getConnection()
        try:
            result = await conn.execute(
                f"""INSERT INTO user_auth values ('test_user', $1, 1)""",
                pswdManager.getPasswordHash("password")
            )
            logger.debug(f"{result}")
        except Exception as err:
            logger.warn(err)
        await conn.close()

    async def generateTestUser(self):
        pswdManager = UsersPasswordsManager()
        conn = await getConnection()
        try:
            await conn.execute(
                """INSERT INTO offices (id, location) values (1, 'ул. Колотушкина, д.10');"""
            )
            logger.debug("INSERT INTO offices")
            await conn.execute(
                """INSERT INTO managers (name, surename, patronomic, office_id, role) 
                values ('Иван', 'Иванов', 'Иванович', 1, 'manager');"""
            )
            logger.debug("INSERT INTO managers")
            await conn.execute(
                """INSERT INTO user_auth values ('test_user', $1, 1);""",
                pswdManager.getPasswordHash("password")
            )
            logger.debug("INSERT INTO user_auth")
        except Exception as err:
            logger.warn(err)
        await conn.close()
    
    async def dropTables(self):
        conn = await getConnection()
        for key in self.schema:
                result = await conn.execute(f'''DROP TABLE {key} CASCADE''')
                logger.debug(f"{result} {key}")
        await conn.close()