from jsonschema import validate, ValidationError

from general_module.models import Company

from main.response_processing import unauthorized_response, validate_response, reject_response

from main.session_storage import session_exists
from main.session_storage import get_user, logout_user

from main.licence_packs_managment import get_active_licence_pack


def validate_request(schema):
    def request_dec(func):
        def request_handler(self, request):
            try:
                validate(instance=request.data, schema=schema)
                return func(self, request)
            except ValidationError:
                return reject_response()
        return request_handler
    return request_dec


def validate_session():
    def request_dec(func):
        def request_handler(self, request):
            request_data = request.data
            session = request_data["session"]

            if not session_exists(session):
                return unauthorized_response()

            # Checking the db in order to make sure that there is a company attached to the session:
            elif not Company.objects.filter(guid=get_user(session)):
                logout_user(session)
                return unauthorized_response()

            else:
                return func(self, request)
        return request_handler
    return request_dec


def validate_licence(res_schema, is_add_employee_operation=False):
    def request_dec(func):
        def request_handler(self, request):
            company = Company.objects.filter(guid=get_user(request.data["session"]))[0]
            active_licence = get_active_licence_pack(company)

            if active_licence is None:
                return validate_response({
                    "status": "error",
                    "reason": "licenceExpired"
                }, res_schema)

            licence_employees_boundary_reached = \
                active_licence.company.employees_count >= active_licence.employees_count\
                if is_add_employee_operation\
                else active_licence.company.employees_count > active_licence.employees_count

            if licence_employees_boundary_reached:
                return validate_response({
                    "status": "error",
                    "reason": "licenceEmployeesBoundaryReached"
                }, res_schema)

            return func(self, request)
        return request_handler
    return request_dec
