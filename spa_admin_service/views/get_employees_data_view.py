import json

from rest_framework.views import APIView

from general_module.models import AdminLicense, Company, User, ManageToUser
from main.request_validation import validate_request
from main.response_processing import get_success_response, get_error_response, validate_response
from main.sessions_storage import validate_session, validate_license

req_schema_file = open('../schemas/get_employees_data/request.json')
res_schema_file = open('../schemas/get_employees_data/response.json')

req_schema = json.load(req_schema_file)
res_schema = json.load(res_schema_file)


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_license()
    def post(self, request):
        try:
            session = request.data["session"]
            employees = request.data["employees"]
            employee_data = []
            for employee in employees:
                user = User.objects.filter(guid=employee)

                if not user:
                    employee_data.append({"status": "outUser"})
                else:
                    user = user[0]
                    attached_manager = None
                    if user.position == "worker":
                        manager = ManageToUser.objects.filter(user=user)

                        if manager:
                            attached_manager = manager[0].manager.guid

                    body = {
                        "name": user.full_name,
                        "tgUsername": user.telegram_nick,
                        "role": user.position,
                        "attached_manager": attached_manager
                    }

                    employee_data.append(body)

            return validate_response({"status": "ok",
                                      "employeeData": employee_data}, res_schema)

        except:
            return get_error_response(500)
