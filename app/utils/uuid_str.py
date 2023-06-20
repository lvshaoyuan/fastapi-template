from uuid import uuid4


def use_uuid() -> str:
    """
    生成uuid字符串
    :return:
    """
    return uuid4().hex
