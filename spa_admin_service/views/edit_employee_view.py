from rest_framework.views import APIView

from general_module.models import Employee, Company
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

            employee_with_same_tg_username =\
                Employee.objects.filter(tg_username=tg_username, company=company)

            if employee_with_same_tg_username is not None and\
                    employee_with_same_tg_username[0].guid is not employee.guid:
                return validate_response({"status": "usedTgAccount"}, res_schema)

            # TODO: Here we need to properly handle the role change: manager <-> worker:
            # TODO: m->w => we need to delete all related workers attachments.
            # TODO: w->m => we need to delete attachment to the manager of the employee (if exists).

            employee.initials = initials
            employee.telegram_nick = tg_username
            employee.role = role

            if role is "worker":
                attached_manager = employee_data["attached_manager"]
                # TODO: need to reattach the employee (current employee is worker).
                # TODO: also it is very important to check that role of the attached_manager is 'manager'

            employee.save()
            return validate_response({"status": "ok"}, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
