import datetime

from rest_framework.views import APIView

from general_module.models import Company, Licence

from main.request_validation import validate_request
from main.response_processing import server_error_response, validate_response, cors_response
from main.session_storage import get_user
from main.request_validation import validate_session
from main.licence_packs_managment import get_active_licence_pack, unix_time_millis

from spa_admin_service.schemas.licence.request import req_schema
from spa_admin_service.schemas.licence.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    def post(self, request):
        try:
            session = request.data["session"]
            company = Company.objects.filter(guid=get_user(session))[0]
            licences = Licence.objects.filter(company=company)

            active_licence_pack = get_active_licence_pack(company)

            if active_licence_pack is not None:
                active_licence_pack = active_licence_pack.guid

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
                "serverTime": unix_time_millis(datetime.datetime.utcnow()),
                "activeLicencePack": active_licence_pack,
                "licencePacks": licence_packs
            }, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
