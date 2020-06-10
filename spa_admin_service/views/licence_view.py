import datetime
import json

from rest_framework.views import APIView

from general_module.models import AdminLicense, Company, User, ManageToUser, License
from main.request_validation import validate_request
from main.response_processing import get_success_response, get_error_response, validate_response
from main.sessions_storage import validate_session, validate_license, get_user

req_schema_file = open('../schemas/get_employees_data/request.json')
res_schema_file = open('../schemas/get_employees_data/response.json')

req_schema = json.load(req_schema_file)
res_schema = json.load(res_schema_file)

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return round((dt - epoch).total_seconds() * 1000)


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_license()
    def post(self, request):
        try:
            session = request.data["session"]
            company_name = get_user(session)

            company = Company.objects.filter(name=company_name)[0]

            licence_bd = License.objects.filter(company=company)

            data = []

            for licence in licence_bd:
                start_time = unix_time_millis(
                    datetime.datetime.utcfromtimestamp(licence.start_date.timestamp()))
                end_time = unix_time_millis(
                    datetime.datetime.utcfromtimestamp(licence.end_date.timestamp()))
                data.append({
                    "startTime": start_time,
                    "endTime": end_time,
                    "workersCount": licence.count_of_people
                })

            return validate_response({"licencePacks": data}, res_schema)
        except:
            return get_error_response(500)
