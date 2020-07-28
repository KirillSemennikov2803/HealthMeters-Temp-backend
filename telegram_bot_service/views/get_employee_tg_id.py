from rest_framework.views import APIView

from general_module.models import Employee
from main.response_processing import get_success_response, server_error_response


class UserView(APIView):
    def post(self, request):
        try:
            data = request.data

            employees = data["employees"]

            guid_list = list(employees.keys())

            employees_bd = Employee.objects.filter(guid__in=guid_list)

            for employee in employees_bd:
                employee.telegram_id = employees[employee.guid]
                employee.save()
            return get_success_response()
        except:
            return server_error_response()
