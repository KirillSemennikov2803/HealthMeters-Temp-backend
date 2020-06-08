from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from general_module.models import AdminLicense, Company
from main import response_processing
from main.response_processing import get_success_response, get_error_response
from main.sessions_storage import authorize_user, validate_session


class UserView(APIView):
    def post(self, request):
        try:
            company_name = request.data["companyName"]
            password = request.data["password"]
            company = Company.objects.filter(name=company_name)

            if not company:
                return get_success_response({"status": "error",
                                             "reason": "wrongCompanyName"})

            company = company[0]

            if company.password_hash != password:
                return get_success_response({"status": "error",
                                             "reason": "wrongPassword"})

            return get_success_response({"status": "ok",
                                         "session": authorize_user(company_name)})
        except:
            return get_error_response(500)

    def options(self, request, *args, **kwargs):
        return response_processing.setup_cors_response_headers(Response(status=204))
