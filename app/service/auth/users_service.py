"""
@Time : 2023/5/22 17:12 
@Author : oldlv
@File : users_service.py 
@Description:
"""

from fastapi.security import OAuth2PasswordRequestForm
from tortoise import timezone

from app.api import jwt
from app.common.exception import errors
from app.models.user import Users


async def login(form_data: OAuth2PasswordRequestForm):
    user = await Users.get_or_none(username=form_data.username)
    if not user:
        raise errors.MyValidationError(errors='用户名不存在')
    elif not jwt.verity_password(form_data.password, user.password):
        raise errors.MyValidationError(errors='密码错误')
    elif not user.is_active:
        raise errors.MyValidationError(errors='该用户已被锁定，无法登录')
    user.last_login = timezone.now()
    await user.save()
    access_token = jwt.create_access_token(user.pk)
    return access_token, user
