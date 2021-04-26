from enum import Enum


class ResponseStatus(Enum):
    """
    响应状态的枚举类

    状态类型格式形如:
    Status_Name = (code: int, message: str)
    """
    # Debug
    DEBUG = (10000, 'Debug')

    # 成功
    OK = (20000, '成功')

    # 禁止访问
    FORBIDDEN = (50403, 'Forbidden')

    # 意外错误
    UNEXPECTED_ERROR = (50000, '意外错误')

    # 正常错误
    REQUEST_METHOD_ERROR = (40000, '请求方法错误')
    JSON_DECODE_ERROR = (40001, 'JSON 解析错误')
