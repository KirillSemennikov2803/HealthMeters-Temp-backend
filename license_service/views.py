from datetime import datetime, timedelta

from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from license_service.models import Company, License, CompanyLicense, RenewalLicense
from main.response_processing import get_success_response
from user_service.models import User


class UserView(APIView):
    def post(self, request):
        license_key = request.data["license_key"]
        type_license = request.data["type_license"]
        user_telegram_id = request.data["user_telegram_id"]
        if type_license == "registration":
            license = License.objects.filter(key=license_key)
            if not license:
                get_success_response({"status": "no license"})
            license = license[0]
            if not license.active:
                get_success_response({"status": "overdue license"})
            company_license = CompanyLicense.objects.create(start_time=datetime.now(),
                                                            end_time=datetime.now() + timedelta(days=license.duration))
            company = Company.objects.create(license=company_license)
            user = User.objects.create(telegram_id=user_telegram_id, company=company, position="super_admin")
            get_success_response({"status": "ok"})
        else:
            user = User.objects.filter(telegram_id=user_telegram_id)[0]
            company = user.company
            company_license = company.license
            license = RenewalLicense.objects.filter(key=license_key)
            if not license:
                get_success_response({"status": "no license"})
            license = license[0]
            if not license.active:
                get_success_response({"status": "overdue license"})
            company_license.end_time += timedelta(days=license.duration)
            company_license.count_of_people += license.count_of_people
            company_license.save()
            get_success_response({"status": "ok"})

    def get(self, request):
        params = request.query_params
        telegram_id = params["telegram_id"]
        user = User.objects.filter(telegram_id=telegram_id)[0]
        license = user.company.license
        return get_success_response({"count_of_people": license.count_of_people,
                                     "free_people": license.count_of_people - user.company.active_people,
                                     "end_time": license.end_time})
