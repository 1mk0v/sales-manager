import asyncpg
import logging
from .config import *

logger = logging.getLogger('uvicorn.error')

async def getConnection() -> asyncpg.Connection:
    logger.debug(f"Connecting to 'postgresql://{HOST}:{PORT}?user={USER}&password={PSWD}&dbname={NAME}'...")
    return await asyncpg.connect(
        host=HOST,
        port=PORT,
        user=USER,
        database=NAME,
        password=PSWD
    )