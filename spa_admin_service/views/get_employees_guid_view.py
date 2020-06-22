import json

from rest_framework.views import APIView

from general_module.models import AdminPanelLicence, Company, Employee
from main.request_validation import validate_request
from main.response_processing import get_success_response, get_error_response, get_unauthorized_response, \
    validate_response
from main.sessions_storage import validate_session, get_user, validate_licence

from spa_admin_service.schemas.get_employees_data.request import req_schema
from spa_admin_service.schemas.get_employees_data.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_licence()
    def post(self, request):
        try:
            session = request.data["session"]
            company_name = get_user(session)

            company = Company.objects.filter(name=company_name)

            if not company:
                return get_unauthorized_response()

            company = company[0]

            users = Employee.objects.filter(company=company)

            employees = []

            for user in users:
                employees.append(user.guid)

            return validate_response({"status": "ok",
                                      "employees": employees}, res_schema)
        except:
            return get_error_response(500)
