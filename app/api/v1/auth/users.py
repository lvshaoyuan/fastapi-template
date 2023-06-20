"""
@Time : 2023/5/22 17:02 
@Author : oldlv
@File : users.py 
@Description:
"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api import jwt
from app.common.response.response_schema import response_base, ResponseModel
from app.models.user import Users
from app.schemas.users import Token, response_user_info
from app.service.auth import users_service

users = APIRouter()


@users.post('/login', summary='表单登录', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token, user = await users_service.login(form_data)
    return Token(access_token=token)


@users.get('/userinfo', summary='根据token获取用户信息')
async def get_user_info(current_user: Users = Depends(jwt.get_current_user)):
    return response_base.success(data=current_user, exclude=('password',))