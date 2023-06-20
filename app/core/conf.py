import configparser
import os
import sys
from path import Path
from functools import lru_cache

from pydantic import BaseSettings

from app.config import environment_config

config = configparser.RawConfigParser()


BasePath = Path(__file__).parent.parent.parent
sys.path.insert(0, BasePath)
config.read(os.path.join(BasePath, 'app/conf', f'{environment_config}.ini'), encoding='utf8')


class Settings(BaseSettings):
    """ 配置类 """

    # FastAPI
    TITLE: str = config.get('fastapi', 'TITLE')
    VERSION: str = config.get('fastapi', 'VERSION')
    DESCRIPTION: str = config.get('fastapi', 'DESCRIPTION')
    DOCS_URL: str = config.get('fastapi', 'DOCS_URL')
    OPENAPI_URL: str = config.get('fastapi', 'OPENAPI_URL')
    REDOCS_URL: str = config.get('fastapi', 'REDOCS_URL')

    # 静态文件代理
    STATIC_FILE: bool = config.getboolean('sys', 'STATIC_FILE')

    # Uvicorn
    UVICORN_HOST: str = config.get('sys', 'UVICORN_HOST')
    UVICORN_PORT: int = config.getint('sys', 'UVICORN_PORT')
    UVICORN_RELOAD: bool = config.getboolean('sys', 'UVICORN_RELOAD')

    # DB
    DB_ADD_EXCEPTION_HANDLERS: bool = config.getboolean('mysql', 'DB_ADD_EXCEPTION_HANDLERS')  # 线上环境请使用 False
    DB_AUTO_GENERATE_SCHEMAS: bool = config.getboolean('mysql', 'DB_AUTO_GENERATE_SCHEMAS')  # 线上环境请使用 False
    DB_ECHO: bool = config.getboolean('mysql', 'DB_ECHO')  # 是否显示SQL语句
    DB_HOST: str = config.get('mysql', 'DB_HOST')
    DB_PORT: int = config.getint('mysql', 'DB_PORT')
    DB_USER: str = config.get('mysql', 'DB_USER')
    DB_PASSWORD: str = config.get('mysql', 'DB_PASSWORD')
    DB_DATABASE: str = config.get('mysql', 'DB_DATABASE')
    DB_ENCODING: str = config.get('mysql', 'DB_ENCODING')

    # Redis
    REDIS_HOST: str = config.get('redis', 'REDIS_HOST')
    REDIS_PORT: int = config.getint('redis', 'REDIS_PORT')
    REDIS_PASSWORD: str = config.get('redis', 'REDIS_PASSWORD')
    REDIS_DATABASE: int = config.getint('redis', 'REDIS_DATABASE')
    REDIS_TIMEOUT: int = config.getint('redis', 'REDIS_TIMEOUT')

    # Captcha
    CAPTCHA_EXPIRATION_TIME: int = config.getint('captcha', 'CAPTCHA_EXPIRATION_TIME')  # 单位：s

    # Token
    TOKEN_ALGORITHM: str = config.get('token', 'TOKEN_ALGORITHM')  # 加密算法
    TOKEN_SECRET_KEY: str = config.get('token', 'TOKEN_SECRET_KEY')  # 密钥 secrets.token_urlsafe(32))
    TOKEN_EXPIRE_MINUTES: int = config.getint('token', 'TOKEN_EXPIRE_MINUTES')  # 单位：min

    # Email
    EMAIL_DESCRIPTION: str = config.get('email', 'EMAIL_DESCRIPTION')  # 默认发件说明
    EMAIL_SERVER: str = config.get('email', 'EMAIL_SERVER')
    EMAIL_PORT: int = config.getint('email', 'EMAIL_PORT')
    EMAIL_USER: str = config.get('email', 'EMAIL_USER')
    EMAIL_PASSWORD: str = config.get('email', 'EMAIL_PASSWORD')  # 授权密码，非邮箱密码
    EMAIL_SSL: bool = config.getboolean('email', 'EMAIL_SSL')  # 是否使用SSL

    # Cookies
    COOKIES_MAX_AGE: int = config.getint('cookies', 'COOKIES_MAX_AGE')  # 单位：s

    # 中间件
    MIDDLEWARE_CORS: bool = config.getboolean('middleware', 'MIDDLEWARE_CORS')
    MIDDLEWARE_GZIP: bool = config.getboolean('middleware', 'MIDDLEWARE_GZIP')
    MIDDLEWARE_ACCESS: bool = config.getboolean('middleware', 'MIDDLEWARE_ACCESS')


@lru_cache()
def get_settings():
    """ 读取配置优化写法 """
    return Settings()


settings = get_settings()
