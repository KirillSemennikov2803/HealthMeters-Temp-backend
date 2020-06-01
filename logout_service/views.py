from rest_framework.views import APIView
from rest_framework.response import Response
from main import response_processing, sessions_storage
from .req_schema import req_schema
from .res_schema import res_schema


class UserView(APIView):
    def post(self, request):
        session_guid = request.data['session']
        sessions_storage.logout_user(session_guid)
        return response_processing.validate_response({}, res_schema)

    def options(self, request, *args, **kwargs):
        return response_processing.setup_cors_response_headers(Response(status=204))
