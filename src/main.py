import config
import logging
import time
from database.generator import DBGenerator
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from auth import routers as auth_routers
from users import routers as users_routers
from auth import config as auth_conf

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
app.add_middleware(SessionMiddleware, secret_key=auth_conf.SECRET_KEY)

app.include_router(auth_routers.router)
app.include_router(users_routers.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logger.info(f'Processing {request.client.host}:{request.client.port} - "{request.method} {request.url}"...')
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.debug(f'Processed in {str(process_time)}s')
    return response

@app.on_event("startup")
async def startUpApp():
    generator = DBGenerator()
    # await generator.dropTables()
    await generator.generateTables()
    await generator.generateTestUser()