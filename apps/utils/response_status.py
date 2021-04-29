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
    MISSING_PARAMETER_ERROR = (40002, '缺少参数')
    BAD_PARAMETER_ERROR = (40003, '参数错误')

    WX_REQUEST_FAIL_ERROR = (40004, '微信服务器请求失败')
    CODE_INVALID_ERROR = (40005, 'code 无效')
    LOGIN_REQUIRED_ERROR = (40006, '需要登陆')
