from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework.views import APIView

from general_module.models import AdminLicense, Company
from main.response_processing import get_success_response, get_error_response


class UserView(APIView):
    def post(self, request):
        try:
            token = request.data["token"]
            company_name = request.data["companyName"]
            password = request.data["password"]

            admin_license = AdminLicense.objects.filter(token=token)

            if not admin_license:
                get_success_response({" status": "error",
                                      "reason": "invalidToken"})
            admin_license = admin_license[0]

            if not admin_license.active:
                get_success_response({" status": "error",
                                      "reason": "activatedToken"})

            company = Company.objects.filter(name=company_name)

            if company:
                get_success_response({" status": "error",
                                      "reason": "usedCompanyName"})

            company = Company.objects.create(name=company_name, password_hash=password)
            return get_success_response({"status": "ok"})
        except:
            return get_error_response(500)
