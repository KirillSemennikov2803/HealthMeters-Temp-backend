import datetime
import json

from rest_framework.views import APIView

from general_module.models import AdminLicense, Company, User, License
from main.guid_generater import generate_user_guid
from main.request_validation import validate_request
from main.response_processing import get_success_response, get_error_response, validate_response
from main.sessions_storage import validate_session, validate_license, get_user

req_schema_file = open('../schemas/add_employee/request.json')
res_schema_file = open('../schemas/add_employee/response.json')

req_schema = json.load(req_schema_file)
res_schema = json.load(res_schema_file)


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_license()
    def post(self, request):
        try:
            session = request.data["session"]
            employee_data = request.data["employeeData"]

            full_name = employee_data["name"]
            tg_nick = employee_data["tgUsername"]
            role = employee_data["role"]

            company_name = get_user(session)

            company = Company.objects.filter(name=company_name)[0]
            guid = generate_user_guid()

            now = datetime.datetime.utcnow()
            license_bd = License.objects.filter(company=company, start_date__lte=now, end_date__gte=now)[0]

            if license_bd.count_of_people >= company.active_people:
                return validate_response({"status": "error",
                                          "reason": "licenceEmployeesBoundaryReached"}, res_schema)

            user = User.objects.create(guid=guid, full_name=full_name, telegram_nick=tg_nick, position=role,
                                       company=company)

            company.active_people += 1
            company.save()
            return validate_response({"status": "ok"}, res_schema)
        except:
            return get_error_response(500)
