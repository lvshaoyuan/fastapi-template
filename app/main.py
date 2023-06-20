import uvicorn
from path import Path
from app.core.conf import settings
from app.core.serve import register_app
from app.common.log import log


app = register_app()

if __name__ == '__main__':
    try:
        uvicorn.run(app=f'{Path(__file__).stem}:app', host=settings.UVICORN_HOST, port=settings.UVICORN_PORT,
                    reload=settings.UVICORN_RELOAD
                    )
    except Exception as e:
        log.error(f'fastapi start filed ❗: {e}')
