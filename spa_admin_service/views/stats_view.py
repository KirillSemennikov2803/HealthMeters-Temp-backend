from rest_framework.views import APIView

from general_module.models import Company
from main.request_validation import validate_request, validate_session
from main.response_processing import cors_response, server_error_response, validate_response
from main.session_storage import get_user
from spa_admin_service.schemas.stats.request import req_schema
from spa_admin_service.schemas.stats.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    def post(self, request):
        try:
            company = Company.objects.filter(guid=get_user(request.data["session"]))[0]
            return validate_response({"employeesCount": company.employees_count}, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
