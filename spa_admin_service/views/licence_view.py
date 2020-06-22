import datetime

from rest_framework.views import APIView

from general_module.models import Company, Licence
from main.request_validation import validate_request
from main.response_processing import get_error_response, validate_response
from main.sessions_storage import validate_session, get_user
from spa_admin_service.schemas.licence.request import req_schema
from spa_admin_service.schemas.licence.response import res_schema


epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return round((dt - epoch).total_seconds() * 1000)


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    def post(self, request):
        try:
            session = request.data["session"]
            company = Company.objects.filter(guid=get_user(session))[0]
            licences = Licence.objects.filter(company=company)

            now = datetime.datetime.utcnow()

            active_licence_pack =\
                Licence.objects.filter(company=company, start_date__lte=now, end_date__gte=now)

            if active_licence_pack is not None:
                active_licence_pack = active_licence_pack[0].guid

            licence_packs = []

            for licence in licences:
                licence_pack = licence.guid
                start_time = unix_time_millis(
                    datetime.datetime.utcfromtimestamp(licence.start_date.timestamp()))
                end_time = unix_time_millis(
                    datetime.datetime.utcfromtimestamp(licence.end_date.timestamp()))
                licence_packs.append({
                    "licencePack": str(licence_pack),
                    "startTime": start_time,
                    "endTime": end_time,
                    "workersCount": licence.count_of_people
                })

            return validate_response({
                "serverTime": unix_time_millis(datetime.datetime.utcfromtimestamp(now.timestamp())),
                "activeLicencePack": active_licence_pack,
                "licencePacks": licence_packs
            }, res_schema)
        except:
            return get_error_response(500)
