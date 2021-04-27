from apps.utils.response_processor import process_response
from apps.utils.response_status import ResponseStatus
from apps.utils.decorator import Protect, RequiredMethod
from apps.location import models as location_model


@Protect
@RequiredMethod('GET')
def get_locations_list(request):
    request.data = {
        'locations': []
    }

    for one in location_model.Location.objects.all():
        request.data['locations'].append({
            'location_id': one.id,
            'location_name': one.name,
            'location_icon': one.icon.url,
            'location_longitude': one.longitude,
            'location_latitude': one.latitude
        })

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
def get_location_detail(request):
    location_id = request.GET.get('location_id')
    if not location_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    location = location_model.Location.objects.filter(id=location_id).first()
    if not location:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    request.data = {
        'location_id': location.id,
        'location_name': location.name,
        'location_introduction': location.introduction,
        'location_remark': location.remark,
        'location_icon': location.icon.url if location.icon else None,
        'location_image': location.image.url if location.image else None,
        'location_address': location.address,
        'location_longitude': location.longitude,
        'location_latitude': location.latitude
    }

    return process_response(request, ResponseStatus.OK)
