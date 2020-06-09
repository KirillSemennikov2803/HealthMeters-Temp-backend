from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from general_module.models import User
from main.response_processing import get_success_response, get_error_response


class UserView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data["telegram_id"]
            user = User.objects.filter(telegram_id=telegram_id)
            if not user:
                return get_success_response({"status": "out of user"})
            position = user[0].position
            return get_success_response({"position": position})
        except:
            return get_error_response(500)
