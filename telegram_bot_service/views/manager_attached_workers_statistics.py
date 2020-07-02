from rest_framework.views import APIView

from general_module.models import Employee, ManagerToWorker, HealthData
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
                last_data = HealthData.objects.filter(employee=subordinate.worker)

                if not last_data:
                    data["users"].append({"initials": subordinate.worker.initials,
                                          "last_temp": None
                                          })
                else:
                    last_data = last_data.last()
                    data["users"].append({"initials": subordinate.worker.initials,
                                          "last_temp": last_data.temperature,
                                          'date': last_data.date
                                          })

            return get_success_response(data)
        except:
            return server_error_response()
