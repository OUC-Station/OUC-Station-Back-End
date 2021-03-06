import json
import logging

from apps.utils.response_processor import process_response
from apps.utils.response_status import ResponseStatus
from apps.utils.decorator import Protect, RequiredMethod, LoginRequired
from apps.account import models as account_models
from apps.bbs import models as bbs_models
from station import settings


logger = logging.getLogger('django')


@RequiredMethod('POST')
@LoginRequired
def post_topic(request):
    request_data = json.loads(request.body)

    title = request_data.get('title')
    content = request_data.get('content')
    anonymous = request_data.get('anonymous')

    if not title or not content:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    if not isinstance(anonymous, bool):
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    account = account_models.Account.objects.filter(openid=request.session['openid']).first()

    topic = bbs_models.Topic(account=account, anonymous=anonymous,
                             title=title, content=content)
    topic.save()

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('GET')
def get_topics(request):
    current = int(request.GET.get('current', 1))

    count = bbs_models.Topic.objects.count()
    total_page = count // settings.TOPICS_PER_PAGE
    if count % settings.TOPICS_PER_PAGE != 0 or total_page == 0:
        total_page += 1

    if current < 1:
        current = 1
    if current > total_page:
        current = total_page

    topics = bbs_models.Topic.objects.filter() \
        .order_by('-create_time')[(current - 1) * settings.TOPICS_PER_PAGE: current * settings.TOPICS_PER_PAGE]

    request.data = {
        'topics': [],
        'current': current,
        'total': total_page,
        'num': len(topics)
    }

    openid = request.session.get('openid')
    for one in topics:
        request.data['topics'].append({
            'topic_id': one.id,
            'anonymous': one.anonymous,
            'account_nickname': one.account.nick_name if not one.anonymous else '????????????',
            'account_avatar': one.account.avatar if not one.anonymous else None,
            'title': one.title,
            'content': one.content,
            'create_time': one.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'count': bbs_models.Comment.objects.filter(topic=one).count(),
            'can_delete': True if openid and openid == one.account.openid else False
        })

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('GET')
def get_topic_detail(request):
    topic_id = request.GET.get('topic_id')
    if not topic_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    topic = bbs_models.Topic.objects.filter(id=topic_id).first()
    if not topic:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    openid = request.session.get('openid')

    request.data = {
        'topic_id': topic.id,
        'anonymous': topic.anonymous,
        'account_nickname': topic.account.nick_name if not topic.anonymous else '????????????',
        'account_avatar': topic.account.avatar if not topic.anonymous else None,
        'title': topic.title,
        'content': topic.content,
        'create_time': topic.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'can_delete': True if openid and openid == topic.account.openid else False,
        'comments': []
    }
    logger.info('openid: {}, topic.account.openid: {}, {}'.format(openid,
                                                                  topic.account.openid,
                                                                  request.data['can_delete']))

    comments = bbs_models.Comment.objects.filter(topic=topic).order_by('create_time')
    for one in comments:
        request.data['comments'].append({
            'anonymous': one.anonymous,
            'account_nickname': one.account.nick_name if not one.anonymous else '????????????',
            'account_avatar': one.account.avatar if not one.anonymous else None,
            'content': one.content,
            'create_time': one.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'can_delete': True if openid and openid == one.account.openid else False
        })

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('POST')
@LoginRequired
def delete_topic(request):
    request_data = json.loads(request.body)

    topic_id = request_data.get('topic_id')
    if not topic_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    topic = bbs_models.Topic.objects.filter(id=topic_id).first()
    if not topic:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    openid = request.session.get('openid')
    if openid != topic.account.openid:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    topic.delete()

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('POST')
@LoginRequired
def post_comment(request):
    request_data = json.loads(request.body)

    topic_id = request_data.get('topic_id')
    content = request_data.get('content')
    anonymous = request_data.get('anonymous')
    if not topic_id or not content:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    if not isinstance(anonymous, bool):
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    topic = bbs_models.Topic.objects.filter(id=topic_id).first()
    if not topic:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    account = account_models.Account.objects.filter(openid=request.session['openid']).first()

    comment = bbs_models.Comment(account=account, anonymous=anonymous,
                                 topic=topic, content=content)
    comment.save()

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('POST')
@LoginRequired
def delete_comment(request):
    request_data = json.loads(request.body)

    comment_id = request_data.get('comment_id')
    if not comment_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    comment = bbs_models.Comment.objects.filter(id=comment_id).first()
    if not comment:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    openid = request.session.get('openid')
    if openid != comment.account.openid:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    comment.delete()

    return process_response(request, ResponseStatus.OK)
