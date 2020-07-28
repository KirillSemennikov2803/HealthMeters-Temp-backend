import configparser

from django.contrib.auth.models import User
from rest_framework.views import APIView

from main.response_processing import server_error_response, get_success_response

config = configparser.ConfigParser()
config.read("config.ini")


class UserView(APIView):
    def post(self, request):
        try:
            data = request.data
            password = data["password"]
            username = data["username"]
            secret_key = data["secret_key"]

            if secret_key != config["Admin"]["secret_key"]:
                return server_error_response()

            admin = User.objects.create_superuser(password=password, username=username)
            admin.save()
            return get_success_response()
        except Exception as er:
            print(er)
            return server_error_response()
