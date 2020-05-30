from django.shortcuts import render
from rest_framework.views import APIView

from main.response_processing import get_success_response
from user_service.models import User, ManageToUser, HealthData


class UserView(APIView):
    def post(self, request):
        _type = request.data["type"]
        telegram_id = request.data["telegram_id"]
        if _type == "manage_statistics":
            user = User.objects.filter(telegram_id=telegram_id)[0]
            subordinates = ManageToUser.objects.filter(manager=user)
            data = {"users": []}
            for subordinate in subordinates:
                last_data = HealthData.objects.filter(user=subordinate.user)
                if not last_data:
                    data["users"].append({"full_name": subordinate.user.full_name,
                                          "last_temp": "Отсутствуют измерения"
                                          })
                last_data = last_data.last()
                data["users"].append({"full_name": subordinate.user.full_name,
                                      "last_temp": last_data.temperature,
                                      'date': last_data.date
                                      })

            return get_success_response(data)

        elif _type == "admin_statistics":
            user = User.objects.filter(telegram_id=telegram_id)[0]
            company = user.company
            workers_count = User.objects.filter(company=company, position='worker').count
            manager_count = User.objects.filter(company=company, position='manager').count
            data = {
                'workers_count': workers_count,
                'manager_count': manager_count
            }
            return get_success_response(data)
