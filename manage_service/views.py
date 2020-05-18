from rest_framework.views import APIView

from main.response_processing import get_error_response


class UserView(APIView):
    def post(self, request):
        try:
            pass
        except:
            return get_error_response(500)