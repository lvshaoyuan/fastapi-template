from fast_captcha import img_captcha
from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse

from app.common.redis import redis_client
from app.core.conf import settings
from app.utils.generate_string import get_uuid

captcha = APIRouter()


@captcha.get('', summary='获取验证码')
async def get_captcha(request: Request):
    img, code = img_captcha()
    uid = get_uuid()
    request.app.state.captcha_uid = uid
    await redis_client.set(uid, code, settings.CAPTCHA_EXPIRATION_TIME)
    return StreamingResponse(content=img, media_type='image/jpeg')


@captcha.get('/test', summary='验证码测试')
async def check_captcha(request: Request):
    try:
        uid = request.app.state.captcha_uid
        code = await redis_client.get(uid)
        return {'code': 200, 'captcha_uid': uid, 'captcha_code': code}
    except AttributeError:
        return {'msg': '请先获取验证码'}
