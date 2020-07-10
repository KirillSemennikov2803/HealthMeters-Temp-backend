from rest_framework.views import APIView

from general_module.models import Employee
from main.response_processing import get_success_response, get_error_response


class UserView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data["telegram_id"]
            company_guid = request.data["company"]

            employee = Employee.objects.filter(telegram_id=telegram_id, company__guid=company_guid)
            if not employee:
                return get_success_response({"status": "no user"})

            role = employee[0].role

            return get_success_response({"role": role})
        except:
            return get_error_response(500)
