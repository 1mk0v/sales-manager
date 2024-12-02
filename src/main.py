import config
import logging
from database.generator import DBGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import routers as auth_routers

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title='BI System API',
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routers.router)


@app.on_event("startup")
async def startUpApp():
    generator = DBGenerator()
    # await generator.dropTables()
    await generator.generateTables()
    await generator.generateTestUser()