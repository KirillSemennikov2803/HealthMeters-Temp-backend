from datetime import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from general_module.models import User, HealthData
from main.response_processing import get_success_response, get_error_response


class UserView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data["telegram_id"]
            temperature = float(request.data["temperature"])
            user = User.objects.filter(telegram_id=telegram_id)[0]
            health_data = HealthData.objects.create(user=user, date=datetime.now(), temperature=temperature)
            return get_success_response({"status": "ok"})
        except:
            return get_error_response(500)
