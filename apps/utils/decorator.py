import json

from typing import Union
from functools import wraps

from apps.utils.response_status import ResponseStatus
from apps.utils.response_processor import process_response


def Protect(func):
    """
    保护函数的异常捕获装饰器
    """
    @wraps(func)
    def wrapper(request):
        try:
            return func(request)
        except json.JSONDecodeError:
            return process_response(request, ResponseStatus.JSON_DECODE_ERROR)

    return wrapper


def RequiredMethod(method: Union[str, list]):
    """
    请求方式限制装饰器

    :param method: 允许的请求方法
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if isinstance(method, str):
                if request.method == method:
                    return func(request)
                else:
                    return process_response(request, ResponseStatus.REQUEST_METHOD_ERROR)
            elif isinstance(method, list):
                if request.method in method:
                    return func(request)
                else:
                    return process_response(request, ResponseStatus.REQUEST_METHOD_ERROR)
            else:
                return process_response(request, ResponseStatus.UNEXPECTED_ERROR)

        return wrapper

    return decorator


def LoginRequired(func):
    """
    要求登陆装饰器
    """
    @wraps(func)
    def wrapper(request):
        if request.session.get('openid', None) is None:
            return process_response(request, ResponseStatus.LOGIN_REQUIRED_ERROR)

        # 正常处理
        return func(request)

    return wrapper
