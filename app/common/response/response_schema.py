#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional, Any, Union, Set, Dict, TypeVar, Generic

from fastapi.encoders import jsonable_encoder
from pydantic import validate_arguments, BaseModel

_JsonEncoder = Union[Set[Union[int, str]], Dict[Union[int, str], Any]]

__all__ = [
    'ResponseModel',
    'response_base'
]


# T = TypeVar("T")
#
#
# class ResponseModel(Generic[T], BaseModel):
#     code: int
#     msg: str
#     data: Optional[T] = None
#
#     class Config:
#         json_encoders = {
#             datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
#         }


class ResponseModel(BaseModel):
    """
    统一返回模型, 可在 FastAPI 接口请求中指定 response_model 及更多操作
    """
    code: int = 2000
    msg: str = 'Success'
    data: Optional[Any] = None

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
        }


class ResponseBase:

    @staticmethod
    def __encode_json(data: Any):
        return jsonable_encoder(
            data,
            custom_encoder={
                datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
            }
        )

    @staticmethod
    @validate_arguments
    def success(*, code: int = 2000, msg: str = 'Success', data: Optional[Any] = None,
                exclude: Optional[_JsonEncoder] = None):
        """
        请求成功返回通用方法

        :param code: 返回状态码
        :param msg: 返回信息
        :param data: 返回数据
        :param exclude: 排除返回数据(data)字段
        :return:
        """
        data = data if data is None else ResponseBase.__encode_json(data)
        return ResponseModel(code=code, msg=msg, data=data).dict(exclude={'data': exclude})

    @staticmethod
    @validate_arguments
    def fail(*, code: int = 2001, msg: str = 'Bad Request', data: Any = None, exclude: Optional[_JsonEncoder] = None):
        data = data if data is None else ResponseBase.__encode_json(data)
        return ResponseModel(code=code, msg=msg, data=data).dict(exclude={'data': exclude})

    @staticmethod
    @validate_arguments
    def response_200(*, msg: str = 'Success', data: Optional[Any] = None, exclude: Optional[_JsonEncoder] = None):
        data = data if data is None else ResponseBase.__encode_json(data)
        return ResponseModel(code=2000, msg=msg, data=data).dict(exclude={'data': exclude})


response_base = ResponseBase()
