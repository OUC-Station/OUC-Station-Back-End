import random
import string
import time

from enum import Enum


class Pattern(Enum):
    Letters = string.ascii_letters
    Digits = string.digits
    Letters_And_Digits = string.ascii_letters + string.digits
    Uppercase = string.ascii_uppercase
    Lowercase = string.ascii_lowercase
    Hexdigits = string.hexdigits
    Uppercase_And_Digits = string.ascii_uppercase + string.digits
    Lowercase_And_Digits = string.ascii_lowercase + string.digits


def generate_random_string(length: int,
                           pattern: Pattern = Pattern.Letters_And_Digits,
                           add_time_prefix: bool = False) -> str:
    """
    根据长度和模式生成随机字符串

    :param length: 长度
    :param pattern: 模式
    :param add_time_prefix: 是否添加时间前缀
    :return: 随机字符串
    """
    result = []

    for i in range(length):
        result.append(random.choice(pattern.value))

    prefix = ''
    if add_time_prefix:
        prefix = time.strftime("%Y%m%d%H%M%S", time.localtime())

    return prefix + ''.join(result)
