from rest_framework.views import APIView

from license_service.models import Company
from main import response_processing
from rest_framework.response import Response
from main.sessions_storage import authorize_user
from .req_schema import req_schema
from .res_schema import res_schema


class UserView(APIView):
    def post(self, request):
        company_name = request.data["company_name"]
        password_hash = request.data["password_hash"]
        company_db = Company.objects.filter(name=company_name)
        if company_db:
            company_db = company_db[0]
            if company_db.password_hash == password_hash:
                body = {
                    "authorized": True,
                    "session": authorize_user(company_name)
                }
            else:
                body = {
                    "authorized": False
                }
        else:
            body = {
                "authorized": False
            }
        return response_processing.validate_response(body, res_schema)

    def options(self, request, *args, **kwargs):
        return response_processing.setup_cors_response_headers(Response(status=204))
