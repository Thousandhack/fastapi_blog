from fastapi import FastAPI
from app.core.config import settings
from app.db.database import database
from starlette.middleware.cors import CORSMiddleware
from app.api.api import api_router
from fastapi.logger import logger
import logging


app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")


@app.on_event("startup")
def connect_db():
    logger.info('连接数据库-------------------------------------------------------')
    database.connect()


@app.on_event("shutdown")
def close_db():
    if not database.is_closed():
        logger.info('关闭数据库-------------------------------------------------------')
        database.close()


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
    # uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


