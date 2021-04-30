from apps.utils.response_processor import process_response
from apps.utils.response_status import ResponseStatus
from apps.utils.decorator import Protect, RequiredMethod
from apps.activity import models as activity_model
from station import settings


@RequiredMethod('GET')
def get_activities_list(request):
    current = int(request.GET.get('current', 1))

    count = activity_model.Activity.objects.count()
    total_page = count // settings.ACTIVITIES_PER_PAGE
    if count % settings.ACTIVITIES_PER_PAGE != 0 or total_page == 0:
        total_page += 1

    if current < 1:
        current = 1
    if current > total_page:
        current = total_page

    activities = activity_model.Activity.objects.filter(display=True) \
        .order_by('-start_time')[(current - 1) * settings.ACTIVITIES_PER_PAGE: current * settings.ACTIVITIES_PER_PAGE]

    request.data = {
        'activities': [],
        'current': current,
        'total': total_page,
        'num': len(activities)
    }

    for one in activities:
        request.data['activities'].append({
            'activity_id': one.id,
            'title': one.title,
            'cover': one.cover.url if one.cover else None,
            'start_time': one.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('GET')
def get_activity_detail(request):
    activity_id = request.GET.get('activity_id')
    if not activity_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    activity = activity_model.Activity.objects.filter(id=activity_id).first()
    if not activity or not activity.display:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    request.data = {
        'activity_id': activity.id,
        'title': activity.title,
        'cover': activity.cover.url if activity.cover else None,
        'content': activity.content,
        'create_time': activity.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'start_time': activity.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }

    return process_response(request, ResponseStatus.OK)
