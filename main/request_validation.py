from .response_processing import get_reject_response
from jsonschema import validate, ValidationError


def validate_request(schema):
    def request_dec(func):
        def request_handler(self, request):
            request_data = request.data
            try:
                validate(instance=request_data, schema=schema)
                # TODO: Create another decorator.
                # if request.data.get("session") is not None:
                #     if not validate_session(request.data.get("session")):
                #         return get_response_reject(request.data.get("session"))
                return func(self, request)
            except ValidationError:
                return get_reject_response()
        return request_handler
    return request_dec

