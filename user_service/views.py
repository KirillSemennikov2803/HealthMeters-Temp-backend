from datetime import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from main.response_processing import get_success_response
from user_service.models import HealthData, User


class UserView(APIView):
    def post(self, request):
        telegram_id = request.data["telegram_id"]
        temperature = float(request.data["type_license"])
        user = User.objects.filter(telegram_id=telegram_id)[0]
        health_data = HealthData.objects.create(user=user, date=datetime.now(),temperature=temperature)
        return get_success_response()
