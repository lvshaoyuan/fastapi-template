"""
@Time : 2023/4/3 10:16 
@Author : oldlv
@File : chatgpt.py 
@Description:
"""
import os
from typing import List, Union, Dict

from app.common.log import log
from app.models.conversation import Conversation
import tiktoken


async def get_conversation_by_id(message_id):
    """
    根据message_id获取对话内容
    :param message_id:
    :return:
    """
    return await Conversation.filter(item_id=message_id).first()


async def update_conversation(item_id: str, messages: list, new_id: str, consume_token: List[int]):
    """
    更新对话内容
    :param id:
    :param messages:
    :param new_id:
    :param consume_token:
    :return:
    """
    # object = await get_conversation_by_id(id)
    # object.id = new_id
    # object.contents = messages
    # object.consume_token.extend(consume_token)
    # await object.save()
    # return object

    await Conversation.filter(item_id=item_id).update(item_id=new_id, contents=messages, consume_token=consume_token)


async def create_conversation(item_id: str, user_id: str | None, title: str, contents: list, consume_token: List[int]):
    """
    创建对话内容
    :param item_id:
    :param user_id:
    :param title:
    :param contents:
    :param consume_token:
    """
    obj = await Conversation.create(title=title, item_id=item_id, user_id=user_id, contents=contents,
                                    consume_token=consume_token)
    return obj


async def num_tokens_from_messages(messages: List[dict], model="gpt-3.5-turbo-0301"):
    """
    计算token
    :param messages:
    :param model:
    :return:
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        log.error("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        log.info("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return await num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def get_proxies(package) -> Union[None | Dict[str, str]]:
    SOCKS_PROXY_HOST = os.getenv("SOCKS_PROXY_HOST")
    SOCKS_PROXY_PORT = os.getenv("SOCKS_PROXY_PORT")
    HTTPS_PROXY = os.getenv("HTTPS_PROXY")
    proxy, proxies = "", None
    if SOCKS_PROXY_HOST and SOCKS_PROXY_PORT:
        SOCKS_PROXY_USERNAME = os.getenv("SOCKS_PROXY_USERNAME")
        SOCKS_PROXY_PASSWORD = os.getenv("SOCKS_PROXY_PASSWORD")
        if SOCKS_PROXY_USERNAME and SOCKS_PROXY_PASSWORD:
            proxy = f"socks5://{SOCKS_PROXY_USERNAME}:{SOCKS_PROXY_PASSWORD}@{SOCKS_PROXY_HOST}:{SOCKS_PROXY_PORT}"
        else:
            proxy = f"socks5://{SOCKS_PROXY_HOST}:{SOCKS_PROXY_PORT}"
    elif HTTPS_PROXY:
        proxy = HTTPS_PROXY
    if package == "httpx" and proxy:
        proxies = {
            "http://": proxy,
            "https://": proxy,
        }
    if package == "openai" and proxy:
        proxies = proxy
    return proxies
