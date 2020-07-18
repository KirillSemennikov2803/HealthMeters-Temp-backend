from rest_framework.views import APIView

from general_module.models import Employee
from main.response_processing import server_error_response, get_success_response


class UserView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data["telegram_id"]
            users = Employee.objects.filter(telegram_id=telegram_id)

            companies = []

            for user in users:
                companies.append({"guid": user.company.guid,
                                  "name": user.company.name})

            return get_success_response({"companies": companies})
        except:
            return server_error_response()
