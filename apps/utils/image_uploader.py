from apps.utils.decorator import RequiredMethod, Protect
from apps.utils.response_processor import process_response
from apps.utils.response_status import ResponseStatus
from apps.utils.random_string_generator import generate_random_string
from station import settings


@RequiredMethod('POST')
def upload(request):
    img = request.FILES.get('img')
    if not img:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    if img.size > settings.IMAGE_MAX_SIZE:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    extension = img.name.split('.')[-1]

    img_name = generate_random_string(10, add_time_prefix=True)
    path = 'media/' + img_name + '.' + extension

    with open(path, 'wb') as f:
        for chunk in img.chunks():
            f.write(chunk)

    request.data = {
        'path': '/' + path
    }

    return process_response(request, ResponseStatus.OK)
