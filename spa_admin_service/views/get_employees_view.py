from rest_framework.views import APIView

from general_module.models import Company, Employee
from main.request_validation import validate_request
from main.request_validation import validate_session, validate_licence
from main.response_processing import server_error_response, validate_response, cors_response
from main.session_storage import get_user
from spa_admin_service.schemas.get_employees.request import req_schema
from spa_admin_service.schemas.get_employees.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_licence(res_schema)
    def post(self, request):
        try:
            company = Company.objects.filter(guid=get_user(request.data["session"]))[0]
            employees_guids = Employee.objects.filter(company=company)

            employees = []

            for employee in employees_guids:
                employees.append(employee.guid)

            return validate_response({
                "status": "ok",
                "employees": employees
            }, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
