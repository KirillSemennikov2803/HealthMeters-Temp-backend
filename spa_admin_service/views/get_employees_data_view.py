from rest_framework.views import APIView

from general_module.models import Employee, ManagerToWorker, Company

from main.request_validation import validate_request
from main.response_processing import server_error_response, validate_response, cors_response
from main.request_validation import validate_session, validate_licence
from main.session_storage import get_user

from spa_admin_service.schemas.get_employees.request import req_schema
from spa_admin_service.schemas.get_employees.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_licence(res_schema)
    def post(self, request):
        try:
            company = Company.objects.filter(guid=get_user(request.data["session"]))[0]
            employees_guids = request.data["employees"]

            # Here we get the employees from the database:
            employees = []

            if not employees_guids:
                Employee.objects.filter(company=company)

            else:
                for employee_guid in employees_guids:
                    employee = Employee.objects.filter(guid=employee_guid, company=company)

                    if employee is not None:
                        employees.append(employee[0])

            # Here we process the database output and pack the employees data:
            employee_data = []

            for employee in employees:
                attached_manager = None

                if employee.role == "worker":
                    manager = ManagerToWorker.objects.filter(worker=employee)

                    if manager is not None:
                        attached_manager = manager[0].manager.guid

                body = {
                    "initials": employee.full_name,
                    "tgUsername": employee.telegram_nick,
                    "role": employee.role,
                    "attachedManager": attached_manager
                }

                employee_data.append(body)

            return validate_response({
                "status": "ok",
                "employeesData": employee_data
            }, res_schema)

        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
