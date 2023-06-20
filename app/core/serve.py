from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.router import v1
from app.common.exception.exception_handler import register_exception
from app.common.redis import redis_client
from app.core.conf import settings, BasePath
from app.middleware import register_middleware
from tortoise.contrib.fastapi import register_tortoise
from app.models import models


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL
    )

    # 注册静态文件
    register_static_file(app)

    # 中间件
    register_middleware(app)

    # 路由
    register_router(app)

    # 数据库
    register_db(app)

    # 初始化服务
    register_init(app)

    # 分页
    register_page(app)

    # 全局异常处理
    register_exception(app)

    return app


db_config = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': settings.DB_HOST,
                'port': settings.DB_PORT,
                'user': settings.DB_USER,
                'password': settings.DB_PASSWORD,
                'database': settings.DB_DATABASE,
                'charset': settings.DB_ENCODING,
                'echo': settings.DB_ECHO
            }
        },
    },
    'apps': {
        'models': {
            'models': [*models],
            'default_connection': 'default',
        },
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


def register_db(app: FastAPI):
    """
    generate_schemas 为True 时 应用程序启动时自动创建数据表
    add_exception_handlers 为True 时 自动添加异常处理程序
    一般情况下，您不需要在生产中使用它们，因为它们会降低性能
    """
    register_tortoise(
        app,
        config=db_config,
        generate_schemas=settings.DB_AUTO_GENERATE_SCHEMAS,
        add_exception_handlers=settings.DB_ADD_EXCEPTION_HANDLERS,
    )


def register_router(app: FastAPI):
    """
    路由

    :param app: FastAPI
    :return:
    """
    app.include_router(v1)


def register_static_file(app: FastAPI):
    """
    静态文件交互开发模式, 生产使用 nginx 静态资源服务

    :param app:
    :return:
    """
    if settings.STATIC_FILE:
        import os
        from fastapi.staticfiles import StaticFiles
        # 判断是否存在app下的static文件夹
        static_path = os.path.join(BasePath, "app/static")
        if not os.path.exists(static_path):
            os.mkdir(static_path)
        app.mount("/static", StaticFiles(directory=static_path), name="static")


def register_init(app: FastAPI):
    """
    初始化redis连接

    :param app: FastAPI
    :return:
    """

    @app.on_event("startup")
    async def startup_event():
        # 连接redis
        await redis_client.init_redis_connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        # 关闭redis连接
        await redis_client.close()


def register_page(app: FastAPI):
    """
    分页查询

    :param app:
    :return:
    """
    add_pagination(app)
