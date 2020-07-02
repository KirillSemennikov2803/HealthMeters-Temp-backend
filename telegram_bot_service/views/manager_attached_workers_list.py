from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework.views import APIView

from general_module.models import Employee, ManagerToWorker
from main.response_processing import get_success_response, server_error_response


class UserView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data["telegram_id"]
            company_guid = request.data["company"]

            manager = Employee.objects.filter(telegram_id=telegram_id, company__guid=company_guid)[0]
            subordinates = ManagerToWorker.objects.filter(manager=manager, worker__company=manager.company)

            data = {"users": []}
            for subordinate in subordinates:
                data["users"].append({"initials": subordinate.worker.initials,
                                      "tg_username": subordinate.worker.tg_username,
                                      "telegram_id": subordinate.worker.telegram_id
                                      })

            return get_success_response(data)
        except:
            return server_error_response()
