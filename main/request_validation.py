from .response_processing import reject_response
from jsonschema import validate, ValidationError

import datetime

from general_module.models import Company, Licence
from main.response_processing import unauthorized_response, validate_response
from main.session_storage import session_exists
from main.session_storage import get_user


def validate_request(schema):
    def request_dec(func):
        def request_handler(self, request):
            request_data = request.data
            try:
                validate(instance=request_data, schema=schema)
                return func(self, request)
            except ValidationError:
                return reject_response()
        return request_handler
    return request_dec


def validate_session():
    def request_dec(func):
        def request_handler(self, request):
            request_data = request.data
            # if request_data.get("session") is None:
            #     return unauthorized_response()
            session = request_data["session"]
            if session_exists(session):
                return func(self, request)
            return unauthorized_response()
        return request_handler
    return request_dec


def validate_licence(res_schema, is_add_employee_operation=False):
    def request_dec(func):
        def request_handler(self, request):
            request_data = request.data
            session = request_data["session"]

            company = Company.objects.filter(guid=get_user(session))
            if not company:
                return unauthorized_response()

            company = company[0]
            now = datetime.datetime.utcnow()
            active_licence =\
                Licence.objects.filter(company=company, start_time__lte=now, end_time__gte=now)

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
