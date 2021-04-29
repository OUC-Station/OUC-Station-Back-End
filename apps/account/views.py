import json
import requests

from apps.utils.response_processor import process_response
from apps.utils.response_status import ResponseStatus
from apps.utils.decorator import Protect, RequiredMethod
from apps.utils.WXBizDataCrypt import WXBizDataCrypt
from apps.account import models as account_models
from station import settings


@RequiredMethod('POST')
def login(request):
    request_data = json.loads(request.body)

    code = request_data.get('code')
    if not code:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    WX_CODE2SESSION_URL = 'https://api.weixin.qq.com/sns/jscode2session'
    parameters = {
        'appid': settings.WX_APPID,
        'secret': settings.WX_SECRET,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    req = requests.get(WX_CODE2SESSION_URL, params=parameters)
    if req.status_code != 200:
        return process_response(request, ResponseStatus.WX_REQUEST_FAIL_ERROR)

    wx_data = json.loads(req.content)
    if wx_data.get('errcode') == 40029:
        return process_response(request, ResponseStatus.CODE_INVALID_ERROR)
    if wx_data.get('errcode') != 0:
        return process_response(request, ResponseStatus.UNEXPECTED_ERROR)

    openid = wx_data.get('openid')
    unionid = wx_data.get('unionid')
    session_key = wx_data.get('session_key')

    account = account_models.Account.objects.filter(openid=openid).first()
    if not account:
        account = account_models.Account(openid=openid, unionid=unionid)
        account.save()

    request.session['openid'] = openid
    request.session['session_key'] = session_key

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('POST')
def update_user_info(request):
    request_data = json.loads(request.body)

    encryptedData = request_data.get('encryptedData')
    iv = request_data.get('encryptedData')

    if not encryptedData or not iv:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    try:
        pc = WXBizDataCrypt(settings.WX_APPID, request.session['session_key'])
        user_info = pc.decrypt(encryptedData, iv)
    except Exception:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)
    if not user_info:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    account = account_models.Account.objects.filter(openid=request.session['openid']).first()
    account.nick_name = user_info.get('nick_name')
    account.avatar = user_info.get('avatar')
    account.save()

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('GET')
def get_status(request):
    request.data = {
        'is_login': False
    }

    if request.session['openid']:
        request.data['is_login'] = True

        account = account_models.Account.objects.filter(openid=request.session['openid']).first()
        request.data['nick_name'] = account.nick_name
        request.data['avatar'] = account.avatar

    return process_response(request, ResponseStatus.OK)
