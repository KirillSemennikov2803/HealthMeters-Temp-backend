from rest_framework.views import APIView

from general_module.models import Employee, ManagerToWorker, Company
from main.request_validation import validate_request
from main.request_validation import validate_session, validate_licence
from main.response_processing import server_error_response, validate_response, cors_response
from main.session_storage import get_user
from spa_admin_service.schemas.get_employees_data.request import req_schema
from spa_admin_service.schemas.get_employees_data.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_licence(res_schema)
    def post(self, request):
        try:
            company = Company.objects.filter(guid=get_user(request.data["session"]))[0]

            # Here we get the employees from the database:
            employees = []

            if request.data.get("employees") is None:
                employees = Employee.objects.filter(company=company)

            else:
                employees_guids = request.data["employees"]

                for employee_guid in employees_guids:
                    employee = Employee.objects.filter(guid=employee_guid, company=company)

                    if employee:
                        employees.append(employee[0])

            # Here we process the database output and pack the employees data:
            employees_data = []

            for employee in employees:
                attached_manager = None

                if employee.role == "worker":
                    manager = ManagerToWorker.objects.filter(worker=employee)

                    if manager:
                        attached_manager = manager[0].manager.guid

                employee_data = {
                    "initials": employee.initials,
                    "tgUsername": employee.tg_username,
                    "role": employee.role
                }

                if employee.role == "worker":
                    employee_data.update({"attachedManager": attached_manager})

                employees_data.append({
                    "employee": employee.guid,
                    "employeeData": employee_data
                })

            return validate_response({
                "status": "ok",
                "employeesData": employees_data
            }, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
