from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework.views import APIView

from main.response_processing import get_success_response
from user_service.models import User, ManageToUser, HealthData


class UserView(APIView):
    def post(self, request):
        user = User.objects.filter(telegram_id=telegram_id)[0]
        company = user.company
        subordinates = User.objects.filter(company=company)
        data = {"users": []}
        for subordinate in subordinates:
            data["users"].append({"full_name": subordinate.user.full_name,
                                  "telegram_nick": subordinate.user.telegram_nick,
                                  "position": subordinate.user.position
                                  })
        return get_success_response(data)
