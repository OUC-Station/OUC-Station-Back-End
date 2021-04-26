import json

from django.http import HttpResponse

from apps.utils.response_status import ResponseStatus


def process_response(request, status: ResponseStatus) -> HttpResponse:
    """
    根据请求 request 中的数据 data 与状态 status 生成 JSON 格式的响应内容,
    包装成 HttpResponse 对象

    其中如果 status 不存在或类型错误, 则以意外错误作为响应状态

    响应内容格式一般如下:
    {
        "code": 20000,
        "msg": "成功",
        "data": {...}
    }

    :param request: Request 对象
    :param status: ResponseStatus 状态枚举
    :return: 响应 HttpResponse 对象
    """
    # 响应内容
    content = {}

    # 响应状态处理
    if not status or not isinstance(status, ResponseStatus):
        status = ResponseStatus.UNEXPECTED_ERROR
    content['code'] = status.value[0]
    content['msg'] = status.value[1]

    # 响应数据处理
    if status == ResponseStatus.OK and hasattr(request, 'data'):
        content['data'] = request.data

    # 响应内容 JSON 格式化
    content = json.dumps(content)
    return HttpResponse(content,
                        content_type='application/json',
                        status='200',
                        charset='utf-8')
