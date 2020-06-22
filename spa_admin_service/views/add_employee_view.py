from rest_framework.views import APIView

from general_module.models import Company, Employee, ManagerToWorker

from main.guid_generator import generate_user_guid
from main.response_processing import server_error_response, validate_response, cors_response
from main.session_storage import get_user
from main.request_validation import validate_request, validate_session, validate_licence

from spa_admin_service.schemas.add_employee.request import req_schema
from spa_admin_service.schemas.add_employee.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_licence(res_schema, True)
    def post(self, request):
        try:
            employee_data = request.data["employeeData"]

            initials = employee_data["initials"]
            tg_username = employee_data["tgUsername"]
            role = employee_data["role"]

            company = Company.objects.filter(guid=get_user(request.data["session"]))[0]

            # Here we check the uniqueness of the tg_username only within one company:
            if Employee.objects.filter(tg_username=tg_username, company=company) is not None:
                return validate_response({
                    "status": "error",
                    "reason": "usedTgAccount"
                }, res_schema)

            if role is "worker":
                attached_manager_guid = employee_data["attachedManager"]
                manager = Employee.objects.filter(guid=attached_manager_guid, company=company)

                if not manager:
                    return validate_response({
                        "status": "error",
                        "reason": "noEmployee"
                    }, res_schema)
                manager = manager[0]

            employee = Employee.objects.create(
                guid=generate_user_guid(),
                initials=initials,
                tg_username=tg_username,
                role=role,
                company=company)

            if role is "worker":
                ManagerToWorker.objects.create(manager=manager, worker=employee)

            company.employees_count += 1
            company.save()
            return validate_response({"status": "ok"}, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
