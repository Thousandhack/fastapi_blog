from pydantic import BaseSettings, AnyHttpUrl
from typing import List
import os


class GlobalSettings(BaseSettings):

    API_V1_STR: str = '/api/v1.0/auth'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 4

    SECRET_KEY = 'af9e8e26914d49873a226849d58195fbd8e79d538ec9ed37e0c15827c1971f09'

    PROJECT_NAME = 'PhoenixV1.0'

    DATABASE_POOL_SIZE = 20

    class Config:
        case_sensitive = True


class DevelopSettings(GlobalSettings):
    # mysql数据库相关配置
    DATABASE_USER: str = 'fastapi'
    DATABASE_PASSWORD: str = '21ops.com'
    DATABASE_HOST: str = '127.0.0.1'
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str = 'fastapi_peewee'

    # redis相关配置
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = 'Antiddos2019'
    REDIS_DB: int = 15

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://192.168.1.233:8000']

    SERVER_NAME: str = '127.0.0.1'
    SERVER_PORT: int = 8000


class ProductionSettings(GlobalSettings):
    # mysql数据库相关配置
    DATABASE_USER: str = 'phoenix'
    DATABASE_PASSWORD: str = 'phoenix2019'
    DATABASE_HOST: str = '127.0.0.1'
    DATABASE_PORT: int = 19306
    DATABASE_NAME: str = 'fastapi'

    # redis相关配置
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = 'Antiddos2019'
    REDIS_DB: int = 0

    SERVER_NAME: str = '127.0.0.1'
    SERVER_PORT: int = 8000


class TestSettings(GlobalSettings):
    # mysql数据库相关配置
    DATABASE_USER: str = 'phoenix'
    DATABASE_PASSWORD: str = 'phoenix2019'
    DATABASE_HOST: str = '127.0.0.1'
    DATABASE_PORT: int = 19306
    DATABASE_NAME: str = 'fastapi'

    # redis相关配置
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = 'Antiddos2019'
    REDIS_DB: int = 0

    SERVER_NAME: str = '127.0.0.1'
    SERVER_PORT: int = 8000


settings_by_name = dict(
    dev=DevelopSettings(),
    pro=ProductionSettings(),
    test=TestSettings()
)

settings = settings_by_name[os.getenv("PHOENIX_ENV", "dev")]




