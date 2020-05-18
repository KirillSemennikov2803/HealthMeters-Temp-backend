from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from user_service.models import User


class UserView(APIView):
    def post(self, request):
        type = request["type"]
        telegram_id = request["telegram_id"]
        full_name = request['full_name']
        user = User.objects.filter(telegram_id = telegram_id)[0]
        user

        if type == "add":
