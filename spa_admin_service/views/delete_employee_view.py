from rest_framework.views import APIView

from general_module.models import Company, Employee
from main.request_validation import validate_request, validate_session, validate_licence
from main.response_processing import server_error_response, validate_response, cors_response
from main.session_storage import get_user
from spa_admin_service.schemas.delete_employee.request import req_schema
from spa_admin_service.schemas.delete_employee.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_licence(res_schema)
    def post(self, request):
        try:
            company = Company.objects.filter(guid=get_user(request.data["session"]))[0]
            # Here we filter the employees only within one company:
            employee = Employee.objects.filter(guid=request.data["employee"], company=company)

            if not employee:
                return validate_response({
                    "status": "error",
                    "reason": "noEmployee"
                }, res_schema)

            else:
                employee = employee[0]

            employee.delete()

            company.employees_count -= 1
            company.save()
            return validate_response({"status": "ok"}, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
