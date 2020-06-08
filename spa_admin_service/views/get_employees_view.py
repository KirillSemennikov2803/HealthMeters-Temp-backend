from rest_framework.views import APIView

from general_module.models import AdminLicense, Company
from main.response_processing import get_success_response, get_error_response
from main.sessions_storage import validate_session


class UserView(APIView):
    @validate_session
    def post(self, request):

        pass