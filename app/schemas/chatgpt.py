"""
@Time : 2023/4/3 10:07 
@Author : oldlv
@File : chatgpt.py 
@Description:
"""
from typing import Optional

from pydantic import BaseModel, Field


class ChatProcessOptions(BaseModel):
    parentMessageId: str = Field(default="", description="父消息ID")


class ChatProcessRequest(BaseModel):
    prompt: str = Field(default="", description="当前消息")
    options: ChatProcessOptions = Field(default=ChatProcessOptions(), description="选项")
    systemMessage: str = Field(default="You are ChatGPT, a large language model trained by OpenAI. Follow the user's "
                                       "instructions carefully. Respond using markdown.", description="系统设定")
    temperature: float = Field(default=0.8, ge=0, le=1, description="temperature")
    top_p: float = Field(default=1, description="top_p")


class ChatProcessResponse(BaseModel):
    role: str = Field(default="", description="角色")
    id: str = Field(default="", description="openai消息id")
    parentMessageId: str = Field(default="", description="自定义消息id")
    text: str = Field(default="", description="消息回复内容")
    delta: str = Field(default="", description="消息追加内容")
    detail: dict = Field(default={}, description="openai返回内容")
    question_token: int = Field(default=0, description="问题消耗的token")
    answer_token: int = Field(default=0, description="回答消耗的token")


class SessionData(BaseModel):
    auth: bool = Field(default=False, description="是否有鉴权")
    model: str = Field(default="ChatGPTAPI", description="接口模式")


class SessionResponse(BaseModel):
    status: str = Field(default="Success", description="返回状态, Success: 正常 Fail: 异常")
    message: str = Field(default="", description="返回信息")
    data: SessionData = Field(default=SessionData(), description="数据")



