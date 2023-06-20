import random
import re


def search_string(pattern, text) -> bool:
    """
    全字段正则匹配

    :param pattern:
    :param text:
    :return:
    """
    result = re.search(pattern, text)
    if result:
        return True
    else:
        return False


def match_string(pattern, text) -> bool:
    """
    从字段开头正则匹配

    :param pattern:
    :param text:
    :return:
    """
    result = re.match(pattern, text)
    if result:
        return True
    else:
        return False


def is_mobile(text: str) -> bool:
    """
    检查手机号码

    :param text:
    :return:
    """
    return match_string(r"^1[3-9]\d{9}$", text)


def is_wechat(text: str) -> bool:
    """
    检查微信号

    :param text:
    :return:
    """
    return match_string(r"^[a-zA-Z]([-_a-zA-Z0-9]{5,19})+$", text)


def is_qq(text: str) -> bool:
    """
    检查QQ号

    :param text:
    :return:
    """
    return match_string(r"^[1-9][0-9]{4,10}$", text)


def get_invite_code6():
    """
    随机生成6位大写的邀请码:8614LY
    """
    random_str = get_random_set(6)
    return random_str.upper()


def get_random_set(bits):
    """
    生成随机得指定位数 字母+数字字符串
    bits:数字是几就生成几位
    """
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    total_set = num_set + char_set
    value_set = "".join(random.sample(total_set, bits))
    return value_set
