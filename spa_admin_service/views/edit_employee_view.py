from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from general_module.models import AdminLicense, Company, User
from main import response_processing
from main.response_processing import get_success_response, get_error_response
from main.sessions_storage import authorize_user, validate_session, validate_license, get_user


class UserView(APIView):
    @validate_session()
    @validate_license()
    def post(self, request):
        try:
            employee_guid = request.data["employeeGuid"]
            employee_data = request.data["employeeData"]

            user = User.objects.filter(guid=employee_guid)

            if not user:
                return get_success_response({"status": "error",
                                             "reason": "outTgAccount"})

            full_name = employee_data["name"]
            tg_nick = employee_data["tgNick"]
            position = employee_data["role"]

            user = user[0]

            user.full_name = full_name
            user.telegram_nick = tg_nick
            user.position = position

            check_full_name = User.objects.filter(full_name=full_name)
            check_telegram_nick = User.objects.filter(telegram_nick=tg_nick)
            if not check_full_name or not check_telegram_nick:
                return get_success_response({"status": "usedTgAccount"})
            user.save()

            return get_success_response({"status": "ok"})
        except:
            return get_error_response(500)
