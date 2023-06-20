"""
@Time : 2023/3/28 21:28 
@Author : oldlv
@File : chatgpt.py 
@Description:
"""
import asyncio
import concurrent.futures
import json
import traceback

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

# from starlette.responses import StreamingResponse
from app.common.log import log
from app.schemas.chatgpt import ChatProcessRequest, ChatProcessResponse, SessionResponse
from app.service import chatgpt
import openai
import asyncio

from app.service.chatgpt import get_proxies

router = APIRouter()
stream_response_headers = {
    "Content-Type": "application/octet-stream",
    "Cache-Control": "no-cache",
    "Transfer-Encoding": "chunked",
}
openai.api_base = "https://oldlv.work/v1"
openai.api_key = "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"


async def generate(model, messages, data, chat_response):
    params = {
        "model": model,
        "messages": messages,
        'temperature': data.temperature,
        'top_p': data.top_p,
        'stream': True,
    }

    chat_reply_process = await _chat_completions_create_async(params)
    for index, chat in enumerate(chat_reply_process):
        detail = chat.to_dict_recursive()
        choice = detail.get("choices")[0]
        delta = choice.get("delta")
        if not chat_response.role:
            chat_response.role = delta.get("role", "")
        if not chat_response.id:
            chat_response.id = detail.get("id", "")
        chat_response.text += delta.get("content", "")
        chat_response.delta = delta
        chat_response.detail = detail
        chat_response.answer_token = await chatgpt.num_tokens_from_messages(
            [{"role": "system", "content": chat_response.text}], model=model)
        response = chat_response.json(ensure_ascii=False)

        yield f"\n{response}" if index else response

    consume_token = [chat_response.question_token, chat_response.answer_token]
    messages.append({"role": chat_response.role, "content": chat_response.text})
    # 更新会话消息
    if data.options.parentMessageId:
        try:
            # 存在父消息ID，更新会话消息
            await chatgpt.update_conversation(item_id=data.options.parentMessageId, messages=messages,
                                              new_id=chat_response.id, consume_token=consume_token)
        except Exception as e:
            log.error(
                f"Update error: id={data.options.parentMessageId} new_id={chat_response.id} consume_token:{consume_token} messages={messages}")
            log.error(f"Update error reason: {e.__str__()}")
    else:
        try:
            # 不存在父消息ID，创建会话消息
            result = await chatgpt.create_conversation(item_id=chat_response.id, user_id=None, title=data.prompt,
                                                       contents=messages,
                                                       consume_token=consume_token)
            log.info(
                f"create_conversation-----id:{result.id} title:{result.title} consume_token:{result.consume_token} messages:{result.contents}")
        except Exception as e:
            log.error(f"Create error: id={chat_response.id} consume_token:{consume_token} messages={messages}")
            log.error(f"Create error reason: {e.__str__()}")


@router.post('/chat-process', summary='聊天机器人')
async def chat_process(data: ChatProcessRequest):
    # log.info(data.json(ensure_ascii=False))
    if not data.prompt:
        return "请输入问题"
    chat_response = ChatProcessResponse()
    # 配置对话内容
    messages = []
    if data.options.parentMessageId:
        messages.append(data.options.parentMessageId)
        # 查询上一次对话内容
        db_conversation = await chatgpt.get_conversation_by_id(message_id=data.options.parentMessageId)
        if db_conversation:
            messages = db_conversation.contents
    if not messages:
        messages.append({"role": "system", "content": data.systemMessage})
    print("messages:", messages)
    # 插入最新问题
    messages.append({"role": "user", "content": data.prompt})
    model = "gpt-3.5-turbo-0301"

    # 计算token
    chat_response.question_token = await chatgpt.num_tokens_from_messages(messages=messages, model=model)
    # openai请求参数

    answer_text = generate(model=model, messages=messages, data=data, chat_response=chat_response)

    # 流式响应
    return StreamingResponse(content=answer_text, headers=stream_response_headers, media_type="application/octet-stream")


@router.post('/session', response_model=SessionResponse, summary='session')
async def session():
    response = SessionResponse()
    response.data.auth = False
    return response


def _chat_completions_create(params):
    return openai.ChatCompletion.create(**params)


async def _chat_completions_create_async(params):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                executor, _chat_completions_create, params
            )
        except:
            err = traceback.format_exc()
            log.error(err)
            return None
    return result
