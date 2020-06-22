from rest_framework.response import Response
from rest_framework.views import APIView

from general_module.models import Company, Employee
from main import response_processing
from main.response_processing import get_error_response, validate_response
from main.sessions_storage import validate_session, validate_licence, get_user

from spa_admin_service.schemas.delete_employee.response import res_schema


class UserView(APIView):
    @validate_session()
    @validate_licence()
    def post(self, request):
        try:
            session = request.data["session"]
            employee_guid = request.data["employeeGuid"]

            company_name = get_user(session)

            company = Company.objects.filter(name=company_name)[0]

            user = Employee.objects.filter(guid=employee_guid)

            if not user:
                return validate_response({"status": "error",
                                          "reason": "outTgAccount"}, res_schema)

            user = user[0]

            user.delete()

            company.active_people -= 1
            company.save()
            return validate_response({"status": "ok"}, res_schema)
        except:
            return get_error_response(500)

    def options(self, request, *args, **kwargs):
        return response_processing.setup_cors_response_headers(Response(status=204))
