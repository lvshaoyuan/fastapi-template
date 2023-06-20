"""
@Time : 2023/5/22 17:08 
@Author : oldlv
@File : users.py 
@Description:
"""

from pydantic import BaseModel, create_model
from tortoise.contrib.pydantic import pydantic_model_creator

from app.common.response.response_schema import ResponseModel
from app.models.user import Users

UserInfo = pydantic_model_creator(
    Users,
    exclude=('password',),
    name='UserInfo'
)


class Token(BaseModel):
    code: int = 2000
    msg: str = 'Success'
    access_token: str
    token_type: str = 'bearer'


# 根据token 获取用户信息
response_user_info = create_model(
    'response_user_info',
    data=(UserInfo, ...),
    __base__=ResponseModel
)