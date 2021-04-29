import json

from apps.utils.response_processor import process_response
from apps.utils.response_status import ResponseStatus
from apps.utils.decorator import Protect, RequiredMethod, LoginRequired
from apps.account import models as account_models
from apps.suggestion import models as suggestion_models


@RequiredMethod('POST')
@LoginRequired
def post_suggestion(request):
    request_data = json.loads(request.body)

    content = request_data.get('content')
    if not content:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    account = account_models.Account.objects.filter(openid=request.session['openid']).first()

    suggestion = suggestion_models.Suggestion(account=account, content=content)
    suggestion.save()

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('GET')
@LoginRequired
def get_my_suggestions(request):
    request.data = {
        'suggestions': []
    }

    account = account_models.Account.objects.filter(openid=request.session['openid']).first()
    suggestions = suggestion_models.Suggestion.objects.filter(account=account).order_by('-create_time')

    for one in suggestions:
        request.data['suggestions'].append({
            'content': one.content,
            'create_time': one.create_time,
            'reply': one.reply
        })

    return process_response(request, ResponseStatus.OK)
