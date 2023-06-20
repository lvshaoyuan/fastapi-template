from fastapi import APIRouter

from app.api.v1.auth.users import users
from app.api.v1.chatgpt.chatgpt import router as chatgpt
from app.api.v1.verify.captcha import captcha

v1 = APIRouter(prefix='/v1')

v1.include_router(captcha, prefix='/captcha', tags=['图形验证码'])

v1.include_router(users, prefix='/users', tags=['用户'])

v1.include_router(chatgpt, prefix='', tags=['chatgpt'])
