from django.shortcuts import render
from rest_framework.views import APIView

from user_service.models import User, ManageToUser


class UserView(APIView):
    def post(self, request):
        type = request["type"]
        telegram_id = ["telegram_id"]
        if type == "manage statistics":
            user = User.objects.filter(telegram_id=telegram_id)
            subordinates = ManageToUser.objects.filter(manage=user)
            for subordinate in subordinates:


