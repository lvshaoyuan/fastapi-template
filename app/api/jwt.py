from datetime import datetime, timedelta
from typing import Any, Optional, Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.common.exception.errors import TokenError, AuthorizationError
from app.core.conf import settings
from app.models.user import Users

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')  # 密码加密

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/v1/users/login')  # 指明客户端请求token的地址


def get_hash_password(password: str) -> str:
    """
    使用hash算法加密密码

    :param password: 密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)


def verity_password(plain_password: str, hashed_password: str) -> bool:
    """
    密码校验

    :param plain_password: 要验证的密码
    :param hashed_password: 要比较的hash密码
    :return: 比较密码之后的结果
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Union[int, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    生成加密 token

    :param data: 传进来的值
    :param expires_delta: 增加的到期时间
    :return: 加密token
    """
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(settings.TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires, "sub": str(data)}
    encoded_jwt = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_schema)) -> Users:
    """
    通过token获取当前用户

    :param token:
    :return:
    """
    try:
        # 解密token
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = payload.get('sub')
        if not user_id:
            raise TokenError
    except (jwt.JWTError, ValidationError):
        raise TokenError
    user = await Users.get_or_none(id=user_id)
    if not user:
        raise TokenError
    return user


async def get_current_is_superuser(user: Users = Depends(get_current_user)):
    """
    验证当前用户是否为超级用户

    :param user:
    :return:
    """
    is_superuser = user.is_superuser
    if not is_superuser:
        raise AuthorizationError
    return is_superuser
