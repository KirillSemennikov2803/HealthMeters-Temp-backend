from rest_framework.views import APIView

from general_module.models import Employee, Company, ManagerToWorker
from main.request_validation import validate_request
from main.response_processing import server_error_response, validate_response, cors_response
from main.request_validation import validate_session, validate_licence
from main.session_storage import get_user

from spa_admin_service.schemas.edit_employee.request import req_schema
from spa_admin_service.schemas.edit_employee.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_licence(res_schema)
    def post(self, request):
        try:
            employee_guid = request.data["employee"]
            employee_data = request.data["employeeData"]
            initials = employee_data["initials"]
            tg_username = employee_data["tgUsername"]
            role = employee_data["role"]

            company = Company.objects.filter(guid=get_user(request.data["session"]))[0]
            # Here we filter the employees only within one company:
            employee = Employee.objects.filter(guid=employee_guid, company=company)

            if employee is None:
                return validate_response({
                    "status": "error",
                    "reason": "noEmployee"
                }, res_schema)

            else:
                employee = employee[0]

            employee_with_same_tg_username = \
                Employee.objects.filter(tg_username=tg_username, company=company)

            if employee_with_same_tg_username is not None and \
                    employee_with_same_tg_username[0].guid is not employee.guid:
                return validate_response({"status": "usedTgAccount"}, res_schema)

            # processing change employee role manager -> worker
            if employee.role is "manager" and role is "worker":
                attach_workers = ManagerToWorker.objects.filter(manager=employee)

                for worker in attach_workers:
                    worker.delete()

            if employee.role is "worker" and role is "manager":
                attach_managers = ManagerToWorker.objects.filter(user=employee)

                if attach_managers is not None:
                    for attach_manager in attach_managers:
                        attach_manager.delete()

            employee.initials = initials
            employee.telegram_nick = tg_username
            employee.role = role

            if role is "worker":
                attached_manager_guid = employee_data["attached_manager"]
                manager = Employee.objects.filter(guid=attached_manager_guid)

                if manager is None:
                    return validate_response({
                        "status": "error",
                        "reason": "noEmployee"
                    }, res_schema)

                manager = manager[0]

                if manager.role is not "manager":
                    return validate_response({
                        "status": "error",
                        "reason": "wrongRoles"
                    }, res_schema)

                attach_managers = ManagerToWorker.objects.filter(user=employee)

                for attach_manager in attach_managers:
                    attach_manager.delete()

                ManagerToWorker.objects.create(manager=manager, user=employee)

            employee.save()
            return validate_response({"status": "ok"}, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
