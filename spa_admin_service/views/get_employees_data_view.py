from rest_framework.views import APIView

from general_module.models import AdminLicense, Company, User, ManageToUser
from main.response_processing import get_success_response, get_error_response
from main.sessions_storage import validate_session, validate_license


class UserView(APIView):
    @validate_session()
    @validate_license()
    def post(self, request):
        try:
            session = request.data["session"]
            employees = request.data["employees"]
            employee_data = []
            for employee in employees:
                user = User.objects.filter(guid=employee)

                if not user:
                    employee_data.append({"status": "outUser"})
                else:
                    user = user[0]
                    attached_manager = None
                    if user.position == "worker":
                        manager = ManageToUser.objects.filter(user=user)

                        if manager:
                            attached_manager = manager[0].manager.guid

                    body = {
                        "name": user.full_name,
                        "tgNick": user.telegram_nick,
                        "role": user.position,
                        "attached_manager": attached_manager
                    }

                    employee_data.append(body)

            return get_success_response({"status": "ok",
                                         "employeeData": employee_data})

        except:
            return get_error_response(500)
