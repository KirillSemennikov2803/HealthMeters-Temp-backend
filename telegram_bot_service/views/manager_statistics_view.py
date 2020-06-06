from rest_framework.views import APIView

from main.response_processing import get_success_response
from user_service.models import User, ManageToUser, HealthData


class UserView(APIView):
    def post(self, request):
        telegram_id = request.data["telegram_id"]
        user = User.objects.filter(telegram_id=telegram_id)[0]
        subordinates = ManageToUser.objects.filter(manager=user)
        data = {"users": []}
        for subordinate in subordinates:
            last_data = HealthData.objects.filter(user=subordinate.user)
            if not last_data:
                data["users"].append({"full_name": subordinate.user.full_name,
                                      "last_temp": "Отсутствуют измерения"
                                      })
            else:
                last_data = last_data.last()
                data["users"].append({"full_name": subordinate.user.full_name,
                                  "last_temp": last_data.temperature,
                                  'date': last_data.date
                                  })

        return get_success_response(data)