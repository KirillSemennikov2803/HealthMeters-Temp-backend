from datetime import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from general_module.models import Employee, HealthData
from main.response_processing import get_success_response, get_error_response


class UserView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data["telegram_id"]
            company_guid = request.data["company"]
            temperature = float(request.data["temperature"])

            employee = Employee.objects.filter(telegram_id=telegram_id, company__guid=company_guid)[0]
            HealthData.objects.create(employee=employee, date=datetime.now(), temperature=temperature)

            return get_success_response({"status": "ok"})
        except:
            return get_error_response(500)
