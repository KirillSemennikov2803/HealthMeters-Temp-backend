from rest_framework.views import APIView

from general_module.models import Company
from main.request_validation import validate_request
from main.response_processing import validate_response, server_error_response, cors_response
from main.session_storage import authorize_user
from spa_admin_service.schemas.authorize.request import req_schema
from spa_admin_service.schemas.authorize.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    def post(self, request):
        try:
            company_name = request.data["companyName"]
            password = request.data["password"]
            company = Company.objects.filter(name=company_name)

            if not company:
                return validate_response({
                    "status": "error",
                    "reason": "wrongCompanyName"
                }, res_schema)

            else:
                company = company[0]

            if company.password != password:
                return validate_response({
                    "status": "error",
                    "reason": "wrongPassword"
                }, res_schema)

            else:
                return validate_response({
                    "status": "ok",
                    "session": authorize_user(company.guid)
                }, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
