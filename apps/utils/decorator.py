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
        except Exception:
            return process_response(request, ResponseStatus.UNEXPECTED_ERROR)

    return wrapper
