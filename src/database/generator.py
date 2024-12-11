import logging
from auth.manager import UsersPasswordsManager
from .schemas import (
    user_session, managers, offices, user_auth,
    customers, office_heads, products, reviews, 
    sales
)
from . import getConnection

logger = logging.getLogger('uvicorn.error')

class DBGenerator():

    def __init__(self) -> None:
        self.schema = {
            "offices": offices,
            "managers": managers,
            "user_auth": user_auth,
            "user_session": user_session,
            "customers": customers,
            "office_heads": office_heads,
            "products": products,
            "reviews": reviews,
            "sales": sales
        }
    
    async def generateTables(self):
        logger.info(f"Generating tables...")
        conn = await getConnection()
        for key in self.schema:
            try:
                result = await conn.execute(f"""CREATE TABLE {key} ({self.schema[key]})""")
                logger.debug(f"{result} {key}")
            except Exception as err:
                logger.warning(err)
                logger.warning('Abort!')
        await conn.close()
        logger.debug(f'Connection close')
    
    async def generateManager(self):
        logger.info(f"Generating manager table...")
        conn = await getConnection()
        try:
            result = await conn.execute(
                f"""INSERT INTO managers (name, surename, patronomic, office_id, role) 
                    values ('Иван', 'Иванов', 'Иванович', 1, 'manager')"""
            )
            logger.debug(f"{result}")
        except Exception as err:
            logger.warning(err)
            logger.warning('Abort!')
        await conn.close()
    
    async def generateOffice():
        logger.info(f"Generating office table...")
        conn = await getConnection()
        try:
            result = await conn.execute(
                f"""INSERT INTO offices (id, location) 
                    values (1, 'ул. Колотушкина, д.10')"""
            )
            logger.debug(f"{result}")
        except Exception as err:
            logger.warning(err)
            logger.warning('Abort!')
        await conn.close()

    async def generateUserAuth(self):
        logger.info(f"Generating user_auth table...")
        pswdManager = UsersPasswordsManager()
        conn = await getConnection()
        try:
            result = await conn.execute(
                f"""INSERT INTO user_auth values ('test_user', $1, 1)""",
                pswdManager.getPasswordHash("password")
            )
            logger.debug(f"{result}")
        except Exception as err:
            logger.warning(err)
            logger.warning('Abort!')
        await conn.close()

    async def generateTestUser(self):
        logger.info(f"Generating test_user...")
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
            logger.warning(err)
            logger.warning('Abort!')
        await conn.close()
    
    async def dropTables(self):
        logger.info(f'Droping all tables...')
        conn = await getConnection()
        for key in self.schema:
            result = await conn.execute(f'''DROP TABLE {key} CASCADE''')
            logger.debug(f"{result} {key}")
        await conn.close()