from rest_framework.views import APIView

from main.nickname_to_id_processing import synchronize_data
from main.response_processing import get_success_response, server_error_response


class UserView(APIView):
    def get(self, request):
        try:
            synchronize_data()
            return get_success_response()
        except:
            return server_error_response()

