from django.shortcuts import render
from rest_framework.views import APIView

from main.response_processing import get_success_response
from user_service.models import User, ManageToUser, HealthData


class UserView(APIView):
    def post(self, request):
        type = request["type"]
        telegram_id = request["telegram_id"]
        if type == "manage statistics":
            user = User.objects.filter(telegram_id=telegram_id)
            subordinates = ManageToUser.objects.filter(manage=user)
            data = {"users": []}
            for subordinate in subordinates:
                last_data = HealthData.objects.latest(user=subordinate)
                if not last_data:
                    data["users"].append({"full_name": subordinate.full_name,
                                          "last_temp": "Отсутствуют измерения"
                                          })
                last_data = last_data[0]
                data["users"].append({"full_name": subordinate.full_name,
                                      "last_temp": last_data.temperature
                                      })

                return get_success_response(data)
